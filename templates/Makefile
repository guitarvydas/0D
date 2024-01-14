LIBSRC=libsrc
ODIN_FLAGS ?= -debug -o:none
D2J=0d/odin/das2json/das2json

run: project0D transpile.drawio.json
	./project0D main project0D.drawio $(LIBSRC)/transpile.drawio

project0D.drawio.json: project0D.drawio $(LIBSRC)/transpile.drawio
	$(D2J) project0D.drawio
	odin build . $(ODIN_FLAGS)

transpile.drawio.json: $(LIBSRC)/transpile.drawio
	$(D2J) $(LIBSRC)/transpile.drawio

clean:
	rm -rf project0D project0D.dSYM
