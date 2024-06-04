- WIP
usage:
$ cd ~/projects <--- choose a temp directory where you want this installed
$ git clone https://github.com/guitarvydas/0D/tree/devpy <--- in branch devpy
$ cd 0D/python/test
$ make install
$ make

I'm working on message tracing for a simple case - simple0d4.drawio.

"Make" should try to interpret simple0d4.drawio.json using the (beta) python kernel. [To generate the .json files, you currently need to install Odin, but, you don't need Odin if the .json files are already there (see Makefile for the names of the .json files)].

To do this very manually, you simply need to type "$ make dev0d4", which should do:
  cat ../gensym.py ../datum.py ../message.py ../container.py ../registry.py ../process.py ../0d.py ../std/std.py ../std/lib.py ../std/fakepipe.py ../std/transpiler.py ../std/stock.py ../std/run.py ./main.py > _.py
  python3 _.py "@" main simple0d4.drawio.json


Currently, something looks fishy in the trace. The 4th line down None catches my eye.

Also, I think that there should be 5 messages in the trace, but I see 6.

I had dev0, dev1, dev2, dev3 working before I added the message tracing stuff. I was working on getting arith0d (dev4) to work.

Do you know how to read the Makefile? If not, I will explain...



