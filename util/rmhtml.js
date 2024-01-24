const fs = require ('fs');
const ohm = require ('ohm-js');

let argv;
let srcFileName;

const grammar = ohm.grammar(`
HtmlStripper {
  stripHTML = char+
  char = break | nbsp | italic | bold | span | other

  break = "<br>"
  nbsp = "&nbsp;"
  italic = "<i" attr? ">" value<"</i>"> "</i>"
  bold = "<b" attr? ">" value<"</b>"> "</b>"
  span = "<span" attr? ">" value<"</span>"> "</span>"

  other = any

  value<s> = (~s char)*
  attr = ~">" " " (~">" any)*
}
`);

const semantics = grammar.createSemantics();

// Register the semantic action
semantics.addOperation('stripHTML', {
    stripHTML : function (cs) { return cs.stripHTML ().join (''); },
    break   : function (_) { return " "; },
    nbsp    : function (_) { return " "; },
    italic  : function (_1, _attr, _3, stuff, _5) { return stuff.stripHTML (); },
    bold  : function (_1, _attr, _3, stuff, _5) { return stuff.stripHTML (); },
    span  : function (_1, _attr, _3, stuff, _5) { return stuff.stripHTML (); },
    value : function (s) { return s.stripHTML ().join (''); },
    other   : function (c) { return this.sourceString; },
    _terminal: function () { return this.sourceString; },
    _iter: function (...children) { return children.map(c => c.stripHTML ()); },
});

function main () {
    // top level command, prints on stdout and stderr (if error) then exits with 0 or 1 (OK, or not OK, resp.)
    try {
	argv = require('yargs/yargs')(process.argv.slice(2)).argv;
	srcFileName = argv._[0];
	let src = fs.readFileSync (srcFileName, 'utf-8');
	const match = grammar.match(src);
	if (match.succeeded()) {
	    const strippedResult = semantics(match).stripHTML();
	    console.log(strippedResult);
	} else {
	    throw 'Failed to match input string against the grammar';
	}
    } catch (e) {
	console.error (e.message.trim ());
	process.exit (1);
    }
}    

main ();
