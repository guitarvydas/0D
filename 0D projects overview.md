
# Examples:
https://github.com/guitarvydas/arith0d pdubroy's arith example built using this starter, emits code in 4 dialects: JS,Python,Wasm,CL 
https://github.com/guitarvydas/abc0d simple language built using this sourdough starter
https://github.com/guitarvydas/llm0d - very simple usage of an LLM
https://github.com/guitarvydas/vsh0d Visual Shell (beginnings of)
https://github.com/guitarvydas/delay0d - handling probes and external code in 0D
https://github.com/guitarvydas/helloworld0d - trivial Hello World in 0D, in series and in parallel


# WIP Examples
(these are being worked on, many of these projects use earlier versions of 0D and were laid aside due to "life gets in the way" issues ... anyone welcome to join in)
## ASON Atoms
https://github.com/guitarvydas/ason
## SRW - Stream ReWriter
https://github.com/guitarvydas/srw
## Create a Prolog library for Javascript, from a Scheme program
https://github.com/guitarvydas/scm2js0d
  based on grammar developed in https://guitarvydas.github.io/2020/12/09/OhmInSmallSteps.html
## Markdown as a Programming Language

https://guitarvydas.github.io/2023/09/24/Find-and-Replace-SCN.html
https://github.com/guitarvydas/find-and-replace
## PT Pascal Compiler 2024
## Ceptre Dungeon Crawler
I discussed my understanding of the Ceptre "Dungeon Crawler" example code in a presentation (Jan. 19, 2024, bumped from Jan. 17).  I found that I needed to draw diagrams of my understanding of what the code was doing and sketched them out in the following slides. I am building a 0D drawware version of the diagrams, but, as yet, it is unfinished. Part of the process drove me down a rabbit hole, using 0D to "compile" (generate) Odin code (Leaf components) from some of the diagrams. The code generator ("compiler") is mostly working (gen0D), but needs a very few manual edits before being included in the dc0d project and appeasing the Odin type checker (things like the package name, quoted quotes in a few places, etc.  - not worth spending more time automating, since my manual edits work fine, for now). As it stands, I use 14 simple layers of diagrams to reverse engineer the game.
- presentation https://guitarvydas.github.io/2024/01/19/Ceptre-Dungeon-Crawler-Example-Walk-Through.html
- https://github.com/guitarvydas/dc0d/tree/dev branch "dev"
## Kinopio to Markdown
- convert Kinopio point form notes into markdown
- uses SWI-Prolog to inference Kinopio connections and to arrange the markdown in an indented manner
  - was working with an older version of 0D, needs to be update to newer 0D
  - needs to tweaked to use `jq` in several places
- https://github.com/guitarvydas/kinopio2md






An earlier version of the 0D repo contains a few more manual examples:
https://github.com/guitarvydas/0dproto
- includes:
  - basics - how to use this code w/o creating diagrams
  - drawio - how to compile drawio diagrams to running code
