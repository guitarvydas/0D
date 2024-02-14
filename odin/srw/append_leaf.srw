srw1 {
  chars = char+
  char =
    | applySyntactic<Macro>
    | any

  Macro = "zd.append_leaf"  "(leaves," "zd.Leaf_Template" "{" "name" "=" namestr "," "instantiate" "=" procname "}" ")"

  namestr = string
  string = dq notDQ* dq
  notDQ = ~dq any
  dq = "\""
  procname = firstLetter moreNameLetter*
  firstLetter = letter | "_"
  moreNameLetter = firstLetter | digit
}
