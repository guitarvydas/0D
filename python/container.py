
def container_instantiator (reg, owner, container_name, desc):
    container = make_container (container_name, owner)
    children = []
    children_by_id = {} # not strictly necessary, but, we can remove 1 runtime lookup by "compiling it out" here
    # collect children
    for child_desc in desc ["children"]:
        child_instance = get_component_instance (reg, child_desc ["name"], container)
        children.append (child_instance)
        children_by_id [child_desc ["id"]] = child_instance

    connectors = []
    for proto_conn in desc ["connections"]:
        source_component = None
        target_component = None
        connector = Connector ()
        if proto_conn.dir == "down":
            # JSON: {'dir': 0, 'source': {'name': '', 'id': 0}, 'source_port': '', 'target': {'name': 'Echo', 'id': 12}, 'target_port': ''},
            connector.direction = "down"
            connector.sender = Sender ("", nil, proto_conn.port)
            target_component = children_by_id [proto_conn.target.id]
            if (target_component == None):
                load_error (f"internal error: .Down connection target internal error {proto_conn.target}")
            else:
                connector.receiver = Receiver (target_component.name, target_component.input, c.target_port, target_component)
        elif proto_conn.dir == "across":
            connector.direction = "across"
            source_component = child_id_map [proto_conn.source.id]
            target_component = child_id_map [proto_conn.target.id]
            if source_component == None:
                load_error (f"internal error: .Across connection source not ok {proto_conn.source}")
            else:
                connector.sender = Sender (source_component.name, source_component, c.source_port)
                if target_component == None:
                    load_error (f"internal error: .Across connection target not ok {proto_conn.target}")
                else:
                    connector.receiver = Receiver (target_component.name, target_component.input, c.target_port, target_component)
        elif proto_conn.dir == "up":
            connector.direction = "up"
            source_component = child_id_map[c.source.id]
            if source_component == None:
                print (f"internal error: .Up connection source not ok {proto_conn.source}")
            else:
                connector.sender = Sender (source_component.name, source_component, c.source_port)
                connector.receiver = Receiver ("", container.output, proto_conn.target_port, nil)
        elif proto_conn.dir == "through":
            connector.direction = "through"
            connector.sender = Sender ("", nil, proto_conn.source_port)
            connector.receiver = Receiver ("", container.output, proto_conn.target_port, nil)
            source_component = container
            target_component = container
            
        if (source_component != None) and (target_component != None):
            connectors.append (connector)
        container.connections = connectors
        return container
