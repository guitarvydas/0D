    zd.append_leaf (&leaves, zd.Leaf_Instantiator {
        name = "stdout",
        instantiate = stdout_instantiate,
    })



    zd.append_leaf (leaves, zd.Leaf_Template { name = "1then2", instantiate = deracer_instantiate })
-->
    zd.append_template (templates, zd.Template { name = "1then2", descriptor = deracer_instantiate} )
	
    zd.append_leaf (leaves, zd.Leaf_Template { name = "1then2", instantiate = [i] })
-->
    zd.append_template (templates, zd.Template { name = "1then2", descriptor = $i} )
	
	
