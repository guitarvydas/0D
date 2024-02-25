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
6. install Odin compiler https://odin-lang.org
7. modify the contents of files: (look for "___" and edit name/contents)
	- Makefile
	- main.odin
	- project.drawio (using draw.io)
	- README.md
8. rename ___.drawio to <projectname>.drawio, open it with draw.io
9. close the General tab (click triangle) and open 0D tab for palette of builtin components


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

See Visual Syntax section, below.
# Discord: 
https://discord.gg/4422wwXf5Q

# Examples:
https://github.com/guitarvydas/arith0d pdubroy's arith example built using this starter, emits code in 4 dialects: JS,Python,Wasm,CL 
![](examples/arith0d-main.drawio.svg)


https://github.com/guitarvydas/abc0d simple language built using this sourdough starter
![](examples/abc0d-main.drawio.svg)


https://github.com/guitarvydas/llm0d - very simple usage of an LLM

![](examples/llm0d-main.drawio.svg)

https://github.com/guitarvydas/vsh0d Visual Shell (beginnings of)
![](examples/vsh0d-main.drawio.svg)

https://github.com/guitarvydas/delay0d - handling probes and external code in 0D

![](examples/delay0d-main.drawio.svg)

https://github.com/guitarvydas/helloworld0d - trivial Hello World in 0D, in series and in parallel

![](examples/helloworld0d-main.drawio.svg)



# WIP Examples
(these are being worked on, many of these projects use earlier versions of 0D and were laid aside due to "life gets in the way" issues ... anyone welcome to join in)

## ASON Atoms
https://github.com/guitarvydas/ason

![](examples/ason-main.drawio.svg)


## SRW - Stream ReWriter
https://github.com/guitarvydas/srw

![](examples/srw-main.drawio.svg)

## Create a Prolog library for Javascript, from a Scheme program
https://github.com/guitarvydas/scm2js0d

![](examples/scm2js0d-main.drawio.svg)
  based on grammar developed in https://guitarvydas.github.io/2020/12/09/OhmInSmallSteps.html


## Markdown as a Programming Language

![](examples/find-and-replace-screenshot.png)

![](examples/find-and-replace-main.drawio.svg)

https://guitarvydas.github.io/2023/09/24/Find-and-Replace-SCN.html
https://github.com/guitarvydas/find-and-replace

## PT Pascal Compiler 2024
https://github.com/guitarvydas/ptpascal0d
![](examples/ptpascal0d-main.drawio.svg)

## Ceptre Dungeon Crawler
I discussed my understanding of the Ceptre "Dungeon Crawler" example code in a presentation (Jan. 19, 2024, bumped from Jan. 17).  I found that I needed to draw diagrams of my understanding of what the code was doing and sketched them out in the following slides. I am building a 0D drawware version of the diagrams, but, as yet, it is unfinished. Part of the process drove me down a rabbit hole, using 0D to "compile" (generate) Odin code (Leaf components) from some of the diagrams. The code generator ("compiler") is mostly working (gen0D), but needs a very few manual edits before being included in the dc0d project and appeasing the Odin type checker (things like the package name, quoted quotes in a few places, etc.  - not worth spending more time automating, since my manual edits work fine, for now). As it stands, I use 14 simple layers of diagrams to reverse engineer the game.
- presentation https://guitarvydas.github.io/2024/01/19/Ceptre-Dungeon-Crawler-Example-Walk-Through.html
- https://github.com/guitarvydas/dc0d/tree/dev branch "dev"
- ![](examples/dc0d-Game.drawio.svg)
- https://github.com/guitarvydas/gen0d
- ![](examples/gen0d-main.drawio.svg)

## Kinopio to Markdown
- convert Kinopio point form notes into markdown
- uses SWI-Prolog to inference Kinopio connections and to arrange the markdown in an indented manner
  - was working with an older version of 0D, needs to be update to newer 0D
  - needs to tweaked to use `jq` in several places
- https://github.com/guitarvydas/kinopio2md
- ![](examples/top-main.drawio.svg)





An earlier version of the 0D repo contains a few more manual examples:
https://github.com/guitarvydas/0dproto
- includes:
  - basics - how to use this code w/o creating diagrams
  - drawio - how to compile drawio diagrams to running code
  
---

# 0D - Zero Dependencies - and Drawware

# Details

This version uses the Odin language internally.

More languages are expected.

# Syntax Rules 

This section describes the "syntax" used in our compilable diagrams.

## Overview
In general, the diagrams display a software program as a set of Components interconnected by Connection arrows.

There are two major classes of Component:
- Container
- Leaf.

Containers are drawings that can contain Components and Connections.  Containers can contain other Container components and/or Leaf components.  In `draw.io`, we represent each Container as a separate drawing on a separate *tab* in the `draw.io` editor.

Leaves represent code.  Leaves are represented on diagrams as dark blue rectangles.  The actual code is in other files. In this demo, most of the Leaves are in `leaf0d/leaf0d.odin`.   That's only a convention, not a requirement. The code must provide two entry points
1. instantiate
2. handle

Typically, *handle* uses the *send* function to create output messages.

Components are *templates* (similar to *classes*).  Components can be instantiated multiple times in a project.  Each instantiation is unique and has a blob of unique storage (state) associated with it (similar to *self* in class-based languages).

Templates have unique names.  Instances do not need to be explicitly named. The underlying 0D engine guarantees that each instance is unique (in a manner similar to *references* to *objects* in class-based languages).

Components have input and output *ports*.  Input ports are drawn as white pills (small rounded rectangles), and output ports are drawn as dark-blue pills.  Each port has a unique name.  The names are scoped to be visible only within their parent component.  The scope of input port names is unique from the scope of output port names within the same component, i.e. a component can use the same name for an input port as for an output port, but every input name must be different from every other input name within the same component and every output name must be different from every other output name within the same component.  Different components can use the same names for ports as other components, for example, many components have input ports named "input".  Those port names do not clash, they are "locally scoped" to their parent components.

Containers also have special ports called *gates*.  Gates represent the top-level inputs and outputs of a Container.  Input gates are drawn as white rhombuses with a name, and, output gates are drawn as blue rhombuses with a name.

Connections within Containers are used to hook output ports to input ports of child components in a 1:many and many:1 manner.  And, Connections hook *gates* to *ports*.

Components can only *send* messages to their own output ports and gates.  This is similar to *input parameter lists* in other programming languages, except that the parameter lists are for *outputs* (the set of input ports are like input parameter lists, the set of output ports are like output parameter lists).  In other programming languages, a function cannot know where a particular input parameter came from.  Likewise, a component cannot know where a particular output will go nor where an input came from.

Unlike procedures and functions in most programming languages, inputs to and outputs from a component can happen at any time, in any order.  For example, if a component has two inputs A and B, it might be the case that inputs arrive on port B, and, some time later, inputs arrive on port A, or, the inputs might arrive very closely spaced together in time, or, multiple B inputs might arrive before any A inputs arrive, or, inputs *never* arrive on port A, and so on.

It turned out to be trivial to represent shell commands as Leaf Components.  This repo includes a demo of such components.  We call this VSH - for Visual SHell.  It is possible to draw shell pipelines in `draw.io` and to execute the pipelines.  Combinations beyond simple pipelines are possible to express and are easier to express visually than as pure text.  [*Aside: an outcome of this approach is that it is convenient to visually express component programs that contain relatively heavy concepts.  For example, a parser can be drawn and implemented as a single component with input ports and output ports.  We are considering making A.I. and LLM components.*]
## Visual Overview

First, I list summaries for the various sections, then the details of each section...
### Visual Syntax Summary
- bare component
- Container
- Leaf
- input gate
- output gate 
- input port
- output port
- connection
- VSH component
- comment

#### Notes
- "VSH" means Visual SHell (like a `draw.io` version of */bin/bash*, but simplified).
- *gates* and *ports* are similar, except that *gates* represent inputs and outputs of drawings, where *ports* represent in/out ports of components inside diagrams.
- Containers can contain other Containers or Leaves, Leaves are at the *bottom* and contain nothing but code.
- these diagrams can be found in ../DPL syntax/DPL syntax.drawio.
### Visual Semantics Summary
- down
- up
- across
- through
- fan-out (split)
- fan-in (join)

### Style, Readability Summary
- opacity
- line style
- line thickness

### Idioms Summary
- feedback
- sequential
- parallel
- concurrency
- errors, exceptions

### Low Level Technicalities Summary
- kickoff inject
- handle ()
- send ()
- message copying
- active and idle
- notes

## Visual Syntax
### bare component
![](doc/DPL%20syntax-bare%20component.drawio.svg)
### Container
![](doc/DPL%20syntax-Container.drawio.svg)
### Leaf
![](doc/DPL%20syntax-Leaf.drawio.svg)
### input gate
![](doc/DPL%20syntax-input%20gate.drawio.svg)
### output gate 
![](doc/DPL%20syntax-output%20gate.drawio.svg)
### input port
![](doc/DPL%20syntax-input%20port.drawio.svg)
### output port
![](doc/DPL%20syntax-output%20port.drawio.svg)
### connection
![](doc/DPL%20syntax-connection.drawio.svg)
### VSH component
![](doc/DPL%20syntax-vsh%20component.drawio.svg)
### comment
![](doc/DPL%20syntax-comment.drawio.svg)

## Visual Semantics
### down
![](doc/DPL%20syntax-down.drawio.svg)
### up
![](doc/DPL%20syntax-up.drawio.svg)
### across
![](doc/DPL%20syntax-across.drawio.svg)
### through
![](doc/DPL%20syntax-through.drawio.svg)
### fan-out (split)
![](doc/DPL%20syntax-fan-out%20(split).drawio.svg)
### fan-in (join)
![](doc/DPL%20syntax-fan-in%20(join).drawio.svg)

## Style, Readability
### opacity
![](doc/DPL%20syntax-opacity.drawio.svg)
### line style
![](doc/DPL%20syntax-line%20style.drawio.svg)
### line thickness
![](doc/DPL%20syntax-line%20thickness.drawio.svg)

## Idioms
### feedback
![](doc/DPL%20syntax-feedback.drawio.svg)
### sequential
![](doc/DPL%20syntax-sequential.drawio.svg)
### parallel
![](doc/DPL%20syntax-parallel.drawio.svg)
### concurrency
![](doc/DPL%20syntax-concurrency.drawio.svg)
### errors, exceptions
![](doc/DPL%20syntax-errrors,%20exceptions.drawio.svg)

## Low Leval Technicalities
### kickoff inject
![](doc/DPL%20syntax-kickoff%20inject.drawio.svg)
### handle ()
![](doc/DPL%20syntax-handle().drawio.svg)
### send ()
![](doc/DPL%20syntax-send().drawio.svg)
### message copying
![](doc/DPL%20syntax-message%20copying.drawio.svg)

### active and idle
![](doc/DPL%20syntax-active%20and%20idle.drawio.svg)
### notes
![](doc/DPL%20syntax-notes.drawio.svg)

# Points of Interest

## Das2json

This version of 0D works in two main passes:
1. It converts a draw.io package of drawings (one .drawio file, containing many possible tabs, each containing a drawing) to JSON.
2. It reads the generated JSON and runs the program (by interpreting the information contained in the JSON file.).

Step (1) uses the code in `das2json/*.odin`, while step (2) uses the code in `odin/*/*.odin`.

It is expected that we will be able to replace step (2) with programs written in different languages, like Python, JavaScript, Common Lisp, etc., but, we haven't done so yet.  Ideally, we might rewrite step (2) in a meta language (currently called 'RT' - recursive text) that can then exhale code in Python, JavaScript, Common Lisp, etc., alleviating programmers from porting step (2) code into the various languages manually.  We haven't done this yet.

## Message and Datum

Message is defined as a *3-tuple*:
1. tag
2. data
3. cause.

Tag is some sort of id. In this Odin implementation, the id is a *string*.

Data is a Datum.

Cause is a *2-tuple*
1. the ISU that is handling the message (an `ė` (spelled `eh` in ASCII))
2. the Message being handled.

`ISU` means Isolated Software Unit.  An ISU is a piece of code with 0 dependency leaks. It is like a procedure with a set of inputs *and* a set of outputs.  It cannot call procedures in other ISUs, it can only send messages to other ISUs.  Message sending is like IPCs in processes, not so-called Message Sending in Smalltalk (which is a just a form of subroutine calling with named parameters).  If an ISU calls functions, those functions must be contained within the same ISU.  If you were to draw a diagram of an ISU, it would be a rectangle (or other closed figure) with input ports and output ports (see the blue rectangles with ports in the above diagrams). The ports are not hard-wired to other parts of the system.  An ISU is totally isolated and self-contained.  See below for a discussion of parameters.

In 0D, we use the name Component to mean ISU.

`Cause` allows programmers to track the *provenance* of Messages.  Since each Message contains its cause, we can track back to the beginning of time, by following back-links.

A Datum is like a simplified object, with (at least) the following fields:
- data:     DatumData - a lump of data only known/accessible/mutable by the functions associated with this kind of Datum
- clone:   impure_function (^Datum) -> ^Datum -- an impure function that makes a deep copy of the given Datum, ensures that this copy is in the heap, and returns a pointer to this new copy
- reclaim:  proc (^Datum) -- a procedure that garbage collects the given Datum, deeply
- repr:     function (^Datum) -> string -- a function that returns a string representing the contents of the Datum
- kind:     function ()       -> string -- returns a string that uniquely identifies the type of the this Datum
- raw:      function (^Datum) -> []byte -- returns a byte array (essentially a fat pointer) to the contiguous bytes that make up the given Datum (a fat pointer is a pair {pointer,length})

# Project Directories
## Main Body
### src
Contains drawings (i.e. source code), in .drawio format, for the demos
### das2json
Tool that inhales .drawio drawings and exhales .json.

First, of 2, passes in the compilation process.

Foreseen to be used by compiler backends implemented in other languages, like Common Lisp, Python, etc.  But, only the Odin back-end exists at this moment.
### ir
A small set of common definitions used by the front end (das2json) and the back end (odin, at present)
### odin
Implementation of 0D using the Odin language.

Odin is like a "better C".  Programmers need to explicitly write code to manage memory.

Essentially, implementation of 0D in Odin is the most extreme use-case.  Writing 0D in other, garbage-collected, languages should be as easy as simply stripping out the types from the Odin code and changing the syntax.

### llm
LLMs as Components.

Currently, contains only one example - "agency" with hard-wired command line parameters.
## Documentation
### DPL syntax
SVG Diagrams of the syntax.

All of the diagrams are contained in `DPL syntax.drawio` in .drawio format, then exported to SVG.

If changes / updates are needed, one would edit `DPL syntax.drawio`, then export to SVG.
## Future
Beginnings of 0D implementations in other languages.

WIP
### cl
0D in Common Lisp
### rt
0D written in a meta-syntax which I call Recursive Text.  

The goal is to write 0D once - in RT - then use a transpiler technology, like OhmJS + RWR, to exhale 0D in various languages.

I'm still experimenting with what should be, and shouldn't be, in RT. Currently, I believe that there needs to be an explicit differentiation between *operations* and *operands*.  

Operands are basically OOP and functions.  

Operations are "syntax" (probably OhmJS will be used to make this quick and easy).

Pure functions in mathematics can be used to describe *data*, but don't do so well at describing *control flow*.  Data and control flow are two separate issues (data is "shape", control flow is "meaning/stepping-through/interpretation of data").  Currently, in most exiting languages (e.g. Python, Rust, etc.) we use conditional evaluation of functions to fake out control flow.  Yet, conditional evaluation and control flow are very separate issues, that should be treated separately.

Inspiration for this thread of thinking comes from *gcc* and Cordy's *Orthogonal Code Generator* work.  *GCC* uses ideas from Fraser/Davidson peephole technology, namely *RTL*, to make it easier to generate great code.  *OCG* is a further elaboration on such ideas and suggests the design and use of a declarative DSL for expressing code exhalation decision trees. 
# Appendix - Parameters and Return Values

A group of parameters passed to a function in modern languages, is actually just a *single*, contiguous blob of data that is deconstructed into multiple data types.  You can see this in assembler code.  In assembler, we see that values are placed into a array, pointed to be the Stack Pointer.  The parameter list is a heterogenous array (actually a CDR-less List) of various kinds of data.  The receiving procedure immediately deconstructs the bytes in this array and acts like it has several typed data structures in the array.

Likewise, output values are just single, contiguous blobs of data that can be deconstructed into multiple types.

True multiple input parameters, are blobs of data that arrive at *different times* on different ports. True multiple output parameters, are blobs of data that are created at different times on different output ports.

A parameter list in conventional programming languages, is just a single input port.  A complete blob of data arrives - all at once, with no time separation - at the input port.  The receiving procedure / function immediately deconstructs the blob into distinct types of data.  The input data, though, all arrives at once grouped together into a homogenous blob of data, hence, it is but a single input, regardless of how it is deconstructed.

# Appendix - Optimization

Fundamentally, internal language doesn't matter when designing a solution to a problem.

If you need to optimize the solution (a big IF), then internal language and niggly details do matter.  Note that optimization (e.g. type checking, etc.) reduces scalability, hence, should be used sparingly.

# Appendix - About
## Opinions, Gendankener, Author
- Paul Tarvydas
## Odin Implementarian
- Zac Nowicki
## Kibitzers
- Rajiv Abraham
- Boken Lin
- Ken Kan
- in the past, various people at TS Controls - John Shuve, Jeff Roberts, Stephen Gretton, Norm Sanford, Minnan Uppal, Jahan Mazlekzadeh, Ernie doForno, et al. My apologies to those who I've forgotten to mention by name (it's been a while).
# Appendix - Related Technologies
- FBP - Flow Based Programming, J. Paul Morrison
### DPL Syntaxes
DPL means Diagrammatic Programming Languages.

The following DPL syntaxes could be used to describe the innards of ISUs (Isolated Software Units, i.e. Components).  They simply need to be hooked to 0D technology to offer more flexible pluggability.

- Statecharts, Harel
- Drakon
- spreadsheets
- ideas from Jonathan Edwards, such as Subtext

### Editors Which Could Be Used For Writing DPL Programs
DaS means Diagrams as Syntax.  DPL means Diagrammatic Programming Languages.
- draw.io
- Excalidraw
- yEd

### TPL - Textual Programming Languages
N.B. TPLs, such as Python, Rust, Javascript, etc. can, also, be used to write textual code for 0D Components.  See demo_basics above.

### Appendix - Examples for `components_to_include_in_project`
```
components_to_include_in_project :: proc (leaves: ^[dynamic]zd.Leaf_Template) {
    zd.append_leaf (leaves, zd.Leaf_Template { name = "trash", instantiate = trash_instantiate })
    zd.append_leaf (leaves, std.string_constant ("rwr.ohm"))
}
```
