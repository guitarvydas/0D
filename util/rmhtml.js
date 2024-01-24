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
  italic =
    | "<i " tail<"</i>"> -- withattributes
    | "<i>" -- noattributes
    | "</i>" -- end
  bold = 
    | "<b "  tail<"</b>"> -- withattributes
    | "<b>" -- noattributes
    | "</b>" -- end
  span =
    | "<span "  tail<"</span>"> -- withattributes
    | "<span>" -- noattributes
    | "</span>" -- end

  other = any

  tail<s> = (~s any)* s
}
`);

const semantics = grammar.createSemantics();

// Register the semantic action
semantics.addOperation('stripHtml', {
    break   : function (_) { return " "; },
    nbsp    : function (_) { return " "; },
    italic_withattributes  : function (_1, _2) { return ""; },
    italic_noattributes    : function (_1) { return ""; },
    italic_end             : function (_1) { return ""; },
    bold_withattributes    : function (_1, _2) { return ""; },
    bold_noattributes      : function (_1) { return ""; },
    bold_end               : function (_1) { return ""; },
    span_withattributes    : function (_1, _2) { return ""; },
    span_noattributes      : function (_1) { return ""; },
    span_end               : function (_1) { return ""; },
    other   : function (c) { return this.sourceString; },
    _terminal: function () { return this.sourceString; },
    _iter: function (...children) { return children.map(c => c.stripHtml ()); },
});

function main () {
    // top level command, prints on stdout and stderr (if error) then exits with 0 or 1 (OK, or not OK, resp.)
    try {
	argv = require('yargs/yargs')(process.argv.slice(2)).argv;
	srcFileName = argv._[0];
	let src = fs.readFileSync (srcFileName, 'utf-8');
	const match = grammar.match(src);
	if (match.succeeded()) {
	    const strippedResult = semantics(match).stripHtml();
	    console.log(strippedResult.join(''));
	} else {
	    throw 'Failed to match input string against the grammar';
	}
    } catch (e) {
	console.error (e.message.trim ());
	process.exit (1);
    }
}    

main ();
