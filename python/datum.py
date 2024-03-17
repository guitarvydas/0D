class Datum:
  def __init__(self):
    self.data = none
    self.clone = none
    self.reclaim = none
    self.repr = none
    self.kind = none
    self.raw = none

def new_datum_string (s):
    d = Datum ()
    d.data = s
    d.clone = clone_datum_string
    d.reclaim = reclaim_datum_string    
    d.repr = repr_datum_string    
    d.raw = raw_datum_string    
    d.kind = "string"
    return d
}

def clone_datum_string (src):
  d = Datum ()
  d = src
  return d
}

def reclaim_datum_string (src):
  pass

def repr_datum_string (d):
  return d.repr ()

def raw_datum_string (d):
  return d.data



new_datum_bang :: proc () -> ^Datum {
    my_kind :: proc () -> string {
	return "bang"
    }
    p := new (Datum)
    p.data = true
    p.clone = clone_datum_bang
    p.reclaim = reclaim_datum_bang
    p.repr = repr_datum_bang    
    p.raw = raw_datum_bang    
    p.kind = my_kind
    return p
}

clone_datum_bang :: proc (src: ^Datum) -> ^Datum {
    return new_datum_bang ()
}

reclaim_datum_bang :: proc (src: ^Datum) {
}

repr_datum_bang :: proc (src : ^Datum) -> string {
    return "!"
}
raw_datum_bang :: proc (src : ^Datum) -> []byte {
    return transmute([]byte)string("!")
}

///

new_datum_tick :: proc () -> ^Datum {
    my_kind :: proc () -> string {
	return "tick"
    }
    my_clone :: proc (src: ^Datum) -> ^Datum {
	return new_datum_tick ()
    }
    p := new_datum_bang ()
    p.kind = my_kind
    p.clone = my_clone
    p.raw = raw_datum_tick
    return p
}

repr_datum_tick :: proc (src : ^Datum) -> string {
    return "."
}

raw_datum_tick :: proc (src : ^Datum) -> []byte {
    return transmute([]byte)string(".")
}

///
new_datum_bytes :: proc (b : []byte) -> ^Datum {
    my_kind :: proc () -> string {
	return "bytes"
    }
    p := new (Datum)
    p.data = bytes.clone (b)
    p.clone = clone_datum_bytes
    p.reclaim = reclaim_datum_bytes
    p.repr = repr_datum_v
    p.raw = raw_datum_bytes
    p.kind = my_kind
    return p
}

clone_datum_bytes :: proc (src: ^Datum) -> ^Datum {
    p := new (Datum)
    p = src
    p.data = bytes.clone (src.data.([]byte))
    return p
}

reclaim_datum_bytes :: proc (src: ^Datum) {
    // TODO
}

repr_datum_v :: proc (src : ^Datum) -> string {
    return fmt.aprintf ("%v", src.data)
}

raw_datum_bytes :: proc (src: ^Datum) -> []byte {
    return src.data.([]byte)
}


//
new_datum_handle :: proc (h : os.Handle) -> ^Datum {
    my_kind :: proc () -> string {
	return "handle"
    }
    p := new (Datum)
    p.data = h
    p.clone = clone_handle
    p.reclaim = reclaim_handle
    p.repr = repr_datum_v
    p.raw = raw_datum_handle
    p.kind = my_kind
    return p
}

clone_handle :: proc (src: ^Datum) -> ^Datum {
    p := new (Datum)
    p = src
    p.data = src.data.(os.Handle)
    return p
}

reclaim_handle :: proc (src: ^Datum) {
    // TODO
}

raw_datum_handle :: proc (src: ^Datum) -> []byte {
    address := &src.data.(os.Handle)
    nbytes := size_of (os.Handle)
    fmt.assertf (false, "PANIC: raw_datum_handle Not Implemented: address=%v nbytes=%v\n", address, nbytes) 
    return []byte{}
}

//
new_datum_int :: proc (i : int) -> ^Datum {
    my_kind :: proc () -> string {
	return "int"
    }
    p := new (Datum)
    p.data = i
    p.clone = clone_int
    p.reclaim = reclaim_int
    p.repr = repr_datum_v
    p.raw = raw_datum_int
    p.kind = my_kind
    return p
}

clone_int :: proc (src: ^Datum) -> ^Datum {
    p := new (Datum)
    p = src
    p.data = src.data.(int)
    return p
}

reclaim_int :: proc (src: ^Datum) {
    // TODO
}

raw_datum_int :: proc (src: ^Datum) -> []byte {
    address := &src.data.(int)
    nbytes := size_of (int)
    fmt.assertf (false, "PANIC: raw_datum_int Not Implemented: address=%v nbytes=%v\n", address, nbytes) 
    return []byte{}
}
