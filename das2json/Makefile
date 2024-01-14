ODIN_FLAGS ?= -debug -o:none
SYNTAX=syntax/*.odin

das2json: *.odin $(SYNTAX)
	odin build . $(ODIN_FLAGS)

clean:
	rm -rf das2json *.bin *.dSYM *.drawio.json

