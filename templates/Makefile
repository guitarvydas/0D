LIBSRC=libsrc
ODIN_FLAGS ?= -debug -o:none
D2J=0d/odin/das2json/das2json

run: project transpile.drawio.json
	./project main project.drawio $(LIBSRC)/transpile.drawio

project.drawio.json: project.drawio $(LIBSRC)/transpile.drawio
	$(D2J) project.drawio
	odin build . $(ODIN_FLAGS)

transpile.drawio.json: $(LIBSRC)/transpile.drawio
	$(D2J) $(LIBSRC)/transpile.drawio

clean:
	rm -rf project project.dSYM
