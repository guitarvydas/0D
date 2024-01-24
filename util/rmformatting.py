#!/usr/bin/env python3

# strip HTML formatting from input string and print result on stdou
# The intention is to remove formatting that draw.io has inserted into component names, stored in .JSON files
# after compiling .drawio diagrms to .drawio.json output files
import sys

for line in sys.stdin:
    r = line\
      .replace ("<br>", " ")\
      .replace ("<i>", "")\
      .replace (r"<i style=\"\">", "")\
      .replace (r'<span style=\"border-color: var(--border-color);\">', "")\
      .replace ("</span>", "")\
      .replace ('&nbsp;', " ")\
      .replace ("</i>", "")\
      .replace ("⇒", "next (eh, msg)")\
      .replace ("<b>", "")\
      .replace ("</b>", "")
    print (r, end='')
#      .replace (r'<span [^>]*>', "")\
