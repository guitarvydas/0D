LIBSRC=0D/odin/std
ODIN_FLAGS ?= -debug -o:none
D2J=0d/odin/das2json/das2json

run: project transpile.drawio.json
	./project main project.drawio $(LIBSRC)/transpile.drawio

project: project.drawio.json
	odin build . $(ODIN_FLAGS)

project.drawio.json: project.drawio transpile.drawio.json
	$(D2J) project.drawio

transpile.drawio.json: $(LIBSRC)/transpile.drawio
	$(D2J) $(LIBSRC)/transpile.drawio

clean:
	rm -rf project project.dSYM
