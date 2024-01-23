# 0D

drawware: component-based software using diagrams as source code

[0D means "zero dependency" - a prerequisite for using diagrams to create software LEGO(R) blocks]

to create a new project:

1. create a fresh directory for the project
2. cd into the fresh directory and `git init`, then create a submodule with this repo in it
	- `git submodule add https://github.com/guitarvydas/0D`
3. `cp 0D/templates/* .`
4. `mv dot-gitignore .gitignore`
5. `npm install ohm-js yargs`
6. modify the contents of files:
	- Makefile
	- main.odin
	- project.drawio (using draw.io)
	- README.md
7. open (with draw.io) project.drawio
8. close the General tab (click triangle) and open 0D tab for palette of builtin components


Prerequisites, you need to have installed:
- draw.io - [https://www.drawio.com](https://www.drawio.com)
- node.js
- Odin language and compiler https://odin-lang.org

Optional:
- Ohm Editor is a REPL for creating grammars, it can be used in a browser
	- [https://ohmjs.org/editor/](https://ohmjs.org/editor/)
- SWIPL - useful for expressing exhaustive search, instead of using loops within loops
	- SWI Prolog https://www.swi-prolog.org

# DPL Documentation
https://github.com/guitarvydas/0dproto

(scroll down README.md for pictures)

# Discord: 
https://discord.gg/4422wwXf5Q

# Examples:
earlier version of 0D repo:
https://github.com/guitarvydas/0dproto
- includes:
  - arith - @pdubroy's arith.ohm transpiling to WASM, Python, JS, CL
  - LLM - Agency (Emil Valeev) as a single component
  - VSH - Visual Shell
  - abcjs - ridiculously simple language compiled to JS
  - basics - how to use this code w/o creating diagrams
  - drawio - how to compile drawio diagrams to running code
  
# WIP:
- Scheme to Javascript transpiler
  - WIP diary in https://guitarvydas.github.io/2020/12/09/OhmInSmallSteps.html
- Kinopio to markdown converter to LLM
  - WIP in https://github.com/guitarvydas/kinopio2md
- markdown as a programming language syntax
  - prototype https://guitarvydas.github.io/2023/09/24/Find-and-Replace-SCN.html
- macros for non-lisp languages 
  - see https://guitarvydas.github.io/2024/01/05/Macros-for-Non-Lisp-Languages.html)
- PT Pascal upgraded for 2024
  - WIP in https://github.com/guitarvydas/ptpascal0d
- Dungeon Crawler game inspired by Ceptre
  - https://github.com/guitarvydas/ceptre/blob/jan17/presentation/Ceptre%20Walkthrough.pdf
  - WIP in https://github.com/guitarvydas/ceptre/tree/jan17/dc0D (view with drawio) branch "jan17"
