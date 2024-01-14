package zd

import "core:c"
import "core:c/libc"
import "core:strings"
import "core:bytes"
import "core:os"
import "core:fmt"

// `unix_darwin.odin` currently doesn't export an equivalent `Pid` type (yet),
// so we define our own here.
Pid :: distinct i32

foreign import libc_ "system:c"

foreign libc_ {
    waitpid :: proc(pid: Pid, wstatus: rawptr, options: c.int) -> Pid ---
    fork    :: proc() -> Pid ---
    getpid  :: proc() -> Pid ---

    system :: proc(command: cstring) -> c.int ---

    pipe :: proc(fds: [^]os.Handle) -> c.int ---
    dup2 :: proc(fd: os.Handle, fd2: os.Handle) -> c.int ---
    kill :: proc(pid: Pid, sig: c.int)    -> c.int ---

    fcntl :: proc(fd: os.Handle, cmd: c.int, #c_vararg args: ..any) -> c.int ---
}

F_SETFD    :: 2
F_GETFL    :: 3
F_SETFL    :: 4
O_CLOEXEC  :: 524288
O_NONBLOCK :: 2048

unix_pipe :: proc() -> (read: os.Handle, write: os.Handle) {
    fds: [2]os.Handle

    ptr := ([^]os.Handle)(&fds)
    err := pipe(ptr)
    errno := os.get_last_error()
    fmt.assertf(err == 0, "pipe(): %v (%s)", errno, libc.strerror(c.int(errno)))

    read = os.Handle(fds[0])
    write = os.Handle(fds[1])

    fcntl(read, F_SETFD, O_CLOEXEC)
    fcntl(write, F_SETFD, O_CLOEXEC)

    return
}

unix_reopen :: proc(fd, fd2: os.Handle) {
    err := dup2(fd, fd2)
    errno := os.get_last_error()
    fmt.assertf(err >= 0, "dup2() = %d: %v (%s)", err, errno, libc.strerror(c.int(errno)))
}

unix_set_nonblock :: proc(fd: os.Handle) {
    flags: c.int
    fcntl(fd, F_GETFL, &flags)
    fcntl(fd, F_SETFL, flags | O_NONBLOCK)
}

Process_Handle :: struct {
    pid:    Pid,
    input:  os.Handle,
    output: os.Handle,
    error:  os.Handle,
}

process_start :: proc(command: string) -> Process_Handle {
    command_cstr := strings.clone_to_cstring(command, context.temp_allocator)

    // construct pipes for parent/child communication
    stdin_read, stdin_write := unix_pipe()
    stdout_read, stdout_write := unix_pipe()
    stderr_read, stderr_write := unix_pipe()

    fork_pid := fork()

    if fork_pid == 0 {
        unix_reopen(stdin_read, os.Handle(0))
        unix_reopen(stdout_write, os.Handle(1))
        unix_reopen(stderr_write, os.Handle(2))

        // close fds not used by child. without this, we can't close them from
        // the parent process in order to capture their output.
        os.close(stdin_read)
        os.close(stdin_write)
        os.close(stderr_read)
        os.close(stderr_write)

        // TODO(z64): use another pipe to communicate exit status/errno of child
        exit_code := libc.system(command_cstr)

        os.exit(127)
    }

    // close fds used by child
    os.close(stdin_read)
    os.close(stdout_write)
    os.close(stderr_write)

    return {
        pid    = fork_pid,
        input  = stdin_write,
        output = stdout_read,
        error  = stderr_read,
    }
}

process_read_handle :: proc(handle: os.Handle) -> (data: []byte, ok: bool) {
    buffer: bytes.Buffer
    bytes.buffer_init_allocator(&buffer, 0, 0)
    defer if !ok {
        bytes.buffer_destroy(&buffer)
    }
    ok = true
    tmp: [4096]byte
    read_loop: for {
        len, err := os.read(handle, tmp[:])
        switch len {
        case 0:
            break read_loop
        case -1:
            ok = false
            break read_loop
        case:
            bytes.buffer_write(&buffer, tmp[:len])
        }
    }
    if ok {
        data = bytes.buffer_to_bytes(&buffer)
    }
    return
}

process_stop :: proc(hnd: Process_Handle) {
    SIGTERM :: 15
    kill(hnd.pid, SIGTERM)
}

process_wait :: proc(hnd: Process_Handle) -> (ok: bool) {
    waited_pid := waitpid(hnd.pid, nil, 0)
    fmt.assertf(waited_pid == hnd.pid, "waitpid() returned different pid, hnd.pid=%v waited_pid=%v errno=%v", hnd.pid, waited_pid, os.get_last_error())
    return
}

process_destroy_handle :: proc(hnd: Process_Handle) {
    // TODO(z64): ideally, this should avoid doing a double-close.
    // we at least expect outside code to close-off stdin
    os.close(hnd.input)
    os.close(hnd.output)
    os.close(hnd.error)
}

run_command :: proc(cmd: string, input: Maybe(string)) -> (string, string) {
    p := process_start(cmd)

    if input, ok := input.?; ok {
        os.write(p.input, transmute([]byte)input)
    }
    os.close(p.input)

    process_wait(p)

    output, ok_o := process_read_handle(p.output)
    stderr, ok_e := process_read_handle(p.error)

    if !ok_o {
	return "", "read error on stdout"
    } else if !ok_e {
	return "", "read error on stderr"
    } else  {
	return string(output), string(stderr);
    }
}
