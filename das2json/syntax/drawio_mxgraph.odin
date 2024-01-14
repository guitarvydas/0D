package syntax

/*

Routines for taking a draw.io mxgraph XML file and loading them into Page data.
Right now, this is the only supported format. mxGraphs from other drawing
applications may or may not work.

Eventually this API could be normalized to support different sources that can
be coerced into the Page data structure.

*/

import "core:encoding/xml"
import "core:strings"
import "core:slice"
import "core:testing"
import "core:fmt"

Page :: struct {
    name:  string,
    cells: []Cell,
}

Cell :: struct {
    // raw mxgraph values from the document
    mxgraph_id:     string,
    mxgraph_source: string,
    mxgraph_target: string,
    mxgraph_parent: string,
    value:          string,
    // resolved references as indexes into the `page.cells` slice
    id:             int,
    source:         int,
    target:         int,
    parent:         int,
    // detected properties that are useful for making syntaxes
    flags:          Flag_Set,
    type:           Cell_Type,
}

// Various shapes and element types that are detected.
// The order of this enum is used for sorting `page.cells` later.
Cell_Type :: enum {
    Rhombus,
    Rect,
    Ellipse,
    Arrow,
}

// Flags detected from attributes and styles on the element.
Flag_Value :: enum {
    Vertex,
    Edge,
    Container,
}

Flag_Set :: bit_set[Flag_Value]

page_from_elem :: proc(doc: ^xml.Document, elem: xml.Element) -> (page: Page) {
    // find name
    parent0 := doc.elements[elem.parent]
    parent1 := doc.elements[parent0.parent]
    assert(parent1.ident == "diagram", "Unexpected XML layout (root diagram name)")
    for attr in parent1.attribs {
        if attr.key == "name" {
            page.name = attr.val
            break
        }
    }
    assert(page.name != "", "Page without name")

    // find children
    page.cells = make([]Cell, len(elem.value))
    for value, idx in elem.value {
        child_id := value.(xml.Element_ID)
        elem := doc.elements[child_id]
        switch elem.ident {
        case "mxCell":
            page.cells[idx] = cell_from_elem(doc, elem, nil)
        case "UserObject":
            if len(elem.value) > 0 {
                mxcell_child := doc.elements[elem.value[0].(xml.Element_ID)]
                assert(mxcell_child.ident == "mxCell", "Unexpected XML layout (UserObject child is not mxCell)")
                page.cells[idx] = cell_from_elem(doc, mxcell_child, elem)
            }
        case:
            panic("Unexpected XML layout (root children)")
        }
    }

    // sort & assign IDs
    slice.sort_by(page.cells, proc(i, j: Cell) -> bool {
        return i.type < j.type
    })
    for cell, idx in &page.cells {
        cell.id = idx
    }

    // connect source/target references etc.
    for cell in &page.cells {
        for x in page.cells {
            if cell.mxgraph_source == x.mxgraph_id {
                cell.source = x.id
            }
            if cell.mxgraph_target == x.mxgraph_id {
                cell.target = x.id
            }
            if cell.mxgraph_parent == x.mxgraph_id {
                cell.parent = x.id
            }
        }
    }

    return page
}

cell_from_elem :: proc(doc: ^xml.Document, elem: xml.Element, user_object_parent: Maybe(xml.Element)) -> Cell {
    style_kv :: proc(s: string) -> (k, v: string) {
        idx := strings.index(s, "=")
        if idx == -1 {
            k = s
        } else {
            k = s[:idx]
            v = s[idx+1:]
        }
        return k, v
    }

    cell: Cell
    cell.type = .Rect

    for attrib in elem.attribs {
        switch attrib.key {
        case "id":     cell.mxgraph_id = attrib.val
        case "source": cell.mxgraph_source = attrib.val
        case "target": cell.mxgraph_target = attrib.val
        case "parent": cell.mxgraph_parent = attrib.val
        case "value":  cell.value = html_unescape(attrib.val)
        case "vertex": incl(&cell.flags, Flag_Value.Vertex)
        case "edge":
            incl(&cell.flags, Flag_Value.Edge)
            cell.type = .Arrow
        case "style":
            iter := attrib.val
            for kv in strings.split_iterator(&iter, ";") {
                k, _ := style_kv(kv)
                switch k {
                case "ellipse": cell.type = .Ellipse
                case "rhombus": cell.type = .Rhombus
                case "container": incl(&cell.flags, Flag_Value.Container)
                }
            }
        }
    }

    if parent, ok := user_object_parent.?; ok {
        for attrib in parent.attribs {
            switch attrib.key {
            case "id":    cell.mxgraph_id = attrib.val
            case "label": cell.value = attrib.val
            }
        }
    }
    if (cell.type == .Arrow && cell.mxgraph_source == "") {
      fmt.println ("\n###        arrow has no source")
      fmt.println (cell)
    } else if (cell.type == .Arrow && cell.mxgraph_target == "") {
      fmt.println ("\n###        arrow has no target")
      fmt.println (cell)
    }
    return cell
}

// NOTE(z64): This is a best-minimal-effort implementation of unescaping :)
// If you find any other encoded stuff, please feel free to add them to `REPLACEMENTS`.
//
// This currently always makes a new string.
html_unescape :: proc(s: string) -> string {
    REPLACEMENTS :: [][2]string {
        {"&lt;", "<"},
        {"&gt;", ">"},
        {"&amp;", "&"},
        {"&quot;", "\""},
        {"&#39;", "'"},
        {"&#039;", "\\"},
    }

    b := strings.builder_make()
    s := s

    scan_loop: for {
        start := strings.index_rune(s, '&')
        if start == -1 {
            break scan_loop
        }

        end := strings.index_rune(s[start:], ';')
        if end == -1 {
            break scan_loop
        }

        substr := s[start:start+end+1]
        replace_loop: for row in REPLACEMENTS {
            if row[0] == substr {
                strings.write_string(&b, s[:start])
                strings.write_string(&b, row[1])
                s = s[start+end+1:]
                continue scan_loop
            }
        }

        // no replacement found
        strings.write_string(&b, s[:end+1])
        s = s[end+1:]
    }

    if len(s) > 0 {
        strings.write_string(&b, s)
    }
    return strings.to_string(b)
}

@(test)
test_html_unescape :: proc(x: ^testing.T) {
    s := "$ cat &gt;&gt; fortunes.txt"
    e := html_unescape(s)
    testing.expect_value(x, e, "$ cat >> fortunes.txt")
}
