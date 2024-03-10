# Das2JSON

The `das2json` tool compiles drawings from draw.io into JSON.

"DaS" means Diagrams as Syntax.

The intent of this tool is to convert a certain DPL[^dpl] syntax into `.json` files that can be further processed, compiled, transpiled, t2t[^t2t], into running programs.

The intended usage is to draw source code in diagram form - following the rules listed below - and to t2t transpile the diagrams into source code.

In this particular case, we compile to a systems programming language called *Odin*. The compiled Odin code uses the 0D[^0D] library to run the diagrams as 0D software components. This gives the flavour of UNIX-style command-line pipelines, but, at a programming language level. It is expected that the techniques used here can be used to compile and run source code written in DPL format to most other programming languages, like Javascript, Python, WASM, Rust, etc.

Drawings of source code can include concurrency and asynchronous operation of software components. Drawings make concurrency much easier to understand and make it easier to write concurrent programs and to express concurrent operations.

[^dpl]: Diagrammatic Programming Language - a kind of VPL (Visual Programming Language), sans steroids.
[^t2t]: Text to Text translation. This is kind of like macros or FP on steroids. The technique of t2t translation allows converting human-readable "HLL" syntax into a format that is easier to parse automatically, but, is less conveniently-readable to humans. A pipeline of t2t transpilers can be used to implement compilers in a divide-and-conquer fashion, dealing with only one issue at a time, e.g. parsing, semantic info gathering, semantic info checking, allocation, optimization, etc. Each stage in the pipeline can have its own "syntax" that helps it do its job, and, allows earlier stages to remove syntactic noise that is unneeded for automatic compilation, and, allows earlier stages to infer missing bits of information and to make such information explicit and easy to parse.
[^0D]: Zero Dependencies. Over and above the usual explicit software dependencies, the 0D kernel makes it possible to expunge hidden dependencies that appear in most other programming languages, like Python, Rust, etc. These hidden dependencies include issues like strong-coupling through the use of function calls, blocking due to function calls, hard-wired routing decisions due to the use of functions, implicit synchronous operation, etc. In essence, 0D uses software components - written in any programming language - that employ closures and simple message-passing via simple queues, and, do not need to use the usual heavy-handed mechanisms such as full preemption, MMUs, memory-sharing, etc. https://github.com/guitarvydas/0D/tree/main

# Usage

> das2json *file.drawio*

The `das2json` command inhales a `.drawio` file and creates a `.json` file called *file.drawio.json* in the current directory.

The `.json` file can be read and processed using JSON libraries of many popular programming languages, including the `jq` command-line tool.

## Example Usage
The easiest way to look at files produced by this tool is to edit a simple diagram and to edit the `.json` file created by `das2json`. Run 

> das2json examples/example.drawio

and peruse the output file `example.drawio.json`. You can look at the source code using the `draw.io` editor (https://app.diagrams.net) and opening `examples/example.drawio`.

The `example.drawio` file contains 2 diagrams and some comments. One diagram is a sequential arrangement of 2 instances of components, whereas the other diagram is a parallel arrangement of 2 different instances of components. "Comments" are any graphical item that the das2json tools does not recognize - in this case the text boxes containing bold text ("Sequential Routing" and "Parallel Routing") are comments and are ignored by the `das2json` tool.

Zeroing-in on the parallel routing diagram, we should see:

![](examples/example%20screenshot.png)

The generated `example.drawio.json` file contains (partially):
```
[
    {
        "file": "examples/example.drawio",
        "name": "main",
        "children": [
            {
                "name": "Echo",
                "id": 4
            },
            {
                "name": "Echo",
                "id": 6
            },
            {
                "name": "Echo",
                "id": 12
            },
            {
                "name": "Echo",
                "id": 15
            }
        ],
        "connections": [
            {
                "dir": 0,
                "source": {
                    "name": "",
                    "id": 0
                },
                "source_port": "",
                "target": {
                    "name": "Echo",
                    "id": 12
                },
                "target_port": ""
            },
...

```
which describes the 4 instances of components (all derived from the same prototype *Echo*) and connections between the components (the details are discussed below).

For extra examples of the use of the `das2json` tool, see the various example repositories created with the 0D library, such as
- https://github.com/guitarvydas/arith0d
- https://github.com/guitarvydas/abc0d
- https://github.com/guitarvydas/llm0d
- https://github.com/guitarvydas/delay0d
- https://github.com/guitarvydas/vsh0d
- https://github.com/guitarvydas/helloworld0d
- etc.

# Details
## Syntax
Viewing the diagram in the *Examples* section, we see a simple DPL syntax...
- input gates are rhombus figures, with arrows originating from them
- output gates are rhombus figures, with arrow terminating on them
- software components are *draw.io* rectangle containers (flagged by the small "-" in the upper left hand corner - an attribute set on the property sheet of the figure)
- input ports are pill-shaped, rounded rectangles contained by rectangular containers[^containment] that have arrows terminating on them 
- output ports are pill-shaped, rounded rectangles contained by rectangular  containers[^containment] that have arrows originating from them.
- Colours are ignored
- Line-widths are ignored
- Figure sizes are ignored.
- Gates and ports can have text[text] that represents the "port name" (or, "port tag"). In this particular example, there is no need for gate and port names. All of the names are empty strings "".
- Components (container rectangles) have text that represents the prototype ("class") of the component. A unique instance of the prototype is created for each different container rectangle - the container names can be the same (in this case "Echo"), but, the instances are unique for each container figure on the diagram (visually, each container has a different (x,y) position on the diagram. It is *possible* but inadvisable to create containers that perfectly overlap one another, hiding the overlapped containers behind the containers in front).

Note that most of the shapes have been pre-defined and are made available on the `0D` selector on the left-hand toolbar of the `draw.io` editor.

### Conventions
Colours don't matter, and it is unnecessary to know how components are implemented, but, we tend to use...
- Dark blue solid colours for Container components found on other tabs of the editor.
- Gradient blue colours for Containers components that are implemented as *Leaves* in the supporting code, using the base programming language (in this case Odin)
- White colour for input gates and input ports
- Dark blue colour for output gates
- Teal colour for output ports
- 100% opacity for architecturally important arrows
- 2pt thickness  for architecturally important arrows
- 30% opacity for architecturally unimportant arrows required as implementation details
- 1pt thickness for architecturally unimportant arrows required as implementation details
- Gradient red colour for debugging probes
- Gradient yellow colour for "$" shell-out components (see VSH example, mentioned above)
- Gradient blue/gray colour for constant strings (strings are implemented as Components)
- Empty string names for standard input gates and standard input ports (akin to UNIX's *stdin*)
- Empty string names for standard output gates and standard output ports (akin to UNIX's *stdout*)
- The name `✗` ("unicode ballot X") for error ports and gates
- 30% opacity for error ports and gates and their text.

[^containment]: *Draw.io* requires that figures contained in other figures need to be dragged into the boundaries of the containing figure. *Draw.io* denotes capture by highlighting the containers' boundaries in bold, purple during the dragging operation. After a figure has been captured by a container, the figure can be moved partially out of the container, appearing to intersect the edges of the container, as shown in the above diagram.
[^test]: You can insert text into a gate/port/container by double-clicking on the figure and entering text.

## JSON
The `das2json` tool inhales a `.drawio` file and exhales a `.json` file.

A `.drawio` file may contain more than one drawing. Each drawing should be on a separate *tab* in the `draw.io` editor. Each separate drawing represents a *Container* component and must have the same name as a component(s) on some other drawing tab.

One *tab* is reserved as the *top-most* drawing. All other *tabs* represent *Containers* that are used in the project. The name of the *top-most* diagram is arbitrary and must be specified to downstream t2t transpilers.

The output `.json` file contains one JSON Object for each separate *tab* saved out by the `draw.io` editor. Each such Object, contains 4 fields:
- the filename ("file")
- the name of the *tab* ("name")
- a JSON Array of children components found on the diagram. Each child is described with a "name" field and a unique "id" field.
- a JSON Array of connections between the children and the Container. Each connection contains 5 pieces of information:
	- "dir" - the direction of the connection (down, across, up, through (0,1,2,3 resp.))
	- "source" - an Object that contains information about the sourcing component (if the source is the parent Container represented by the diagram, the empty name is used "")
		- "name"
		- "id"
	- "source_port" - the name of the gate/port belonging to the sourcing component
	- "target" - the name of the receiving component ("" for the parent Container itself)
	- "target_port" - the name of the gate/port belonging to the receiving component.

Components that are referenced in the diagrams, but, not implemented on any *tab* are assumed to be *Leaf* components and must be defined in the underlying language using raw textual source code.
### Conventions
- We usually use the name `main` as the tab-name for the top-most diagram in a multiple drawing edit (saved as a single `.drawio` file).

# Authors
Zac Nowicki
Paul Tarvydas
