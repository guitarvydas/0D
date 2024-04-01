compile diagrams to Python, execute the results

(diagram editor == draw.io)

usage: 
- cd <local dir>/0D/python/test
- make

tests: simple00d.drawio simple0d.drawio simple0d2.drawio simple0d3.drawio simple0d4.drawio helloworld0d.drawio vsh0d.drawio arith0d.drawio abc0d.drawio llm0d.drawio

todo: delay0d


see doc/TRACE.md

additions above Odin version:
- project pathname and 0D pathname
- route tracing

TODO:
- draw.io sometimes sprinkles HTML into names and text (component names, port names, gate names) - in the best of all worlds, we should do a recursive-descent parse of anything that looks like HTML and extract/return the non-HTML content (simply deleting the HTML works for 1-level deep HTML, but, doesn't work for HTML wrapped in HTML)

