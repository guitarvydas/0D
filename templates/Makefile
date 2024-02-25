LIBSRC=0D/odin/std
ODIN_FLAGS ?= -debug -o:none
D2J=0d/das2json/das2json

dev: clean run

run: ___ transpile.drawio.json
	./___ main ___testfilename___  ___.drawio $(LIBSRC)/transpile.drawio

___: ___.drawio.json
	odin build . $(ODIN_FLAGS)

___.drawio.json: ___.drawio transpile.drawio.json
	$(D2J) ___.drawio

transpile.drawio.json: $(LIBSRC)/transpile.drawio
	$(D2J) $(LIBSRC)/transpile.drawio

clean:
	rm -rf ___ ___.dSYM *~ *.json
