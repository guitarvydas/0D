# 0D

drawware: component-based software using diagrams as source code

[0D means "zero dependency" - a prerequisite for using diagrams to create software LEGO(R) blocks]

to create a new project:

1. create a fresh directory for the project
2. cd into the fresh directory and create a submodule with this repo in it
	- `git submodule add https://github.com/guitarvydas/0D`
3. `cp 0D/templates/* .`
4. `mv dot-gitignore .gitignore`
5. modify the contents of files:
	- Makefile
	- main.odin
	- project.drawio (using draw.io)
	- README.md
6. open (with draw.io) project.drawio
7. File >> Open Library ... 0D.xml


Prerequisites, you need to have installed:
- draw.io - [https://www.drawio.com](https://www.drawio.com)
- node.js
- ohm-js and yargs `npm install ohm-js yargs`
- Odin language and compiler https://odin-lang.org

Optional:
- Ohm Editor is a REPL for creating grammars, it can be used in a browser
	- [https://ohmjs.org/editor/](https://ohmjs.org/editor/)
- SWIPL - useful for expressing exhaustive search
	- SWI Prolog https://www.swi-prolog.org
