package ir

Container_Decl :: struct {
    file:        string,
    name:        string,
    children:    []Elem_Reference,
    connections: []Connect_Decl,
}

Connect_Decl :: struct {
    dir:         Direction,
    source:      Elem_Reference,
    source_port: string,
    target:      Elem_Reference,
    target_port: string,
}

Direction :: enum {
    Down,
    Across,
    Up,
    Through,
}

Elem_Reference :: struct {
    name: string,
    id:   int,
}

