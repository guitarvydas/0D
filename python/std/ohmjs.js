#!/usr/bin/env node
//'use strict'

// Ohm-JS as a command-line command
//
// an Ohm-JS application consists of 2 operations in sequence
// 1. pattern match
// 2. if the pattern match was successful, then tree-walk the result and apply semantics

const fs = require ('fs');
const ohm = require ('ohm-js');

let argv;
let grammarName;
let grammarFileName;
let rwrFileName;
let currentRuleName = "???";


function makeAST (grammarName, grammarText) {
    // returns an AST object or an error object
    // an AST is an Abstract Syntax Tree, which encodes ALL possible matches
    // in true OO fashion, the AST is further embellished with various methods and
    //  private data, then returned as an internal object
    // returns ast or throws error if any
    //
    // OhmJS converts the text for the grammar into an internal data structure,
    //  that internal data structure is needed for later operations
    // grammarName is used to select only one of the grammars, for matching
    // grammarText contains multiple grammars in textual format
    //
    // the use-case for multiple grammars is, most often, the fact that a grammar
    //  can inherit from other grammars, hence, a grammar text file can contain a number
    //  of uniquely named grammars, only one of which is meant to be used
    //
    let grammars = undefined;
    let ast = undefined;
    let emessage = '';
    try {
	grammars = ohm.grammars (grammarText);
	ast = grammars [grammarName];
	if (ast === undefined) { throw (Error (`can't find grammar ${grammarName} (${grammarName} ${grammarFileName} ${rwrFileName}`)); }
	return ast
    } catch (e) {
	throw (Error (`internal problem: makeAST threw an error\n${grammarName} ${grammarFileName} ${rwrFileName}\n${e.message}`));
    }
}
/////
function patternMatch (src, ast) {
    // return cst or throw error if any
    try {
	matchResult = ast.match (src);
    } catch (e) {
	throw (Error (`internal problem: patternMatch threw an error ${grammarName} ${grammarFileName} ${rwrFileName}\n${e.message}`));
    }
    if (matchResult.failed ()) {
	fs.writeFileSync ('/tmp/patternMatch_src', src);
	throw (Error (`match result failed in patternMatch ${grammarName} ${grammarFileName} ${rwrFileName} (see /tmp/patternMatch_src)\n${matchResult.message}`));
    } else { 
	return matchResult;
    }
}
/////
function makeASST (ast) {
    return ast.createSemantics ();
}
/////
var _traceDepth = 0;
var _tracing = false;

function _ruleInit () {
}

function _traceSpaces () {
    var s = '';
    var n = _traceDepth;
    while (n > 0) {
        s += ' ';
        n -= 1;
    }
    s += `[${_traceDepth.toString ()}]`;
    return s;
}

function _ruleEnter (ruleName) {
    currentRuleName = ruleName;
    if (_tracing) {
        _traceDepth += 1;
        var s = _traceSpaces ();
        s += 'enter: ';
        s += ruleName.toString ();
        console.log (s);
    }
}

function _ruleExit (ruleName) {
    if (_tracing) {
        var s = _traceSpaces ();
        _traceDepth -= 1;
        s += 'exit: ';
        s += ruleName.toString ();
        console.log (s);
    }
}

function extractFormals (s) {
    var s0 = s
        .replace (/\n/g,',')
        .replace (/[A-Za-z0-9_]+ = /g,'')
        .replace (/\.[^;]+;/g,'')
        .replace (/,/,'')
	.replace (/var /g,'')
    ;
    return s0;
}

// helper functions
var ruleName = "???";
function setRuleName (s) { ruleName = s; return "";}
function getRuleName () { return ruleName; }



function hangOperationOntoAsst (asst, opName, opFileName) {
    semanticsFunctionsAsNamespaceString = fs.readFileSync (opFileName, 'utf-8');
    let evalableSemanticsFunctionsString = '(' + semanticsFunctionsAsNamespaceString + ')';
    try {
	compiledSemantics = eval (evalableSemanticsFunctionsString);
	return asst.addOperation (opName, compiledSemantics);
    } catch (e) {
	throw Error (`while loading operation ${opName}: ${evalableSemanticsFunctionsString}: ${e.message}\n$grammarName="{grammarName}" grammFilename="${grammarFileName}" rwrFilename="${rwrFileName}"\n[try using "node ${rwrFileName}", to get better error reporting]`);
    }
}
/////
let src;

function processCST (opName, asst, cst) {
    try {
	return (asst (cst) [opName]) ();
    } catch (e) {
	_tracing = true;
	fs.writeFileSync ('/tmp/src', src);
	throw Error (`error applying semantics [rule "${currentRuleName}" in "${opName}"] during processing of the AST, input src written to /tmp/src\n${e}\ngrammar=${grammarName} grammarFilename=${grammarFileName} semanticsFilename=${rwrFileName}`);
	try {
	    return (asst (cst) [opName]) ();
	} catch (eagain) {
	    throw (`error applying semantics [rule "${currentRuleName}" in "${opName}"] during processing of the AST, input src written to /tmp/src\n${e}\ngrammar=${grammarName} grammarFilename=${grammarFileName} semanticsFilename=${rwrFileName}\n${eagain.message}`);
	}
    }
}
/////

function main () {
    // top level command, prints on stdout and stderr (if error) then exits with 0 or 1 (OK, or not OK, resp.)
    try {
	argv = require('yargs/yargs')(process.argv.slice(2)).argv;
	grammarName = argv._[0];
	grammarFileName = argv._[1];
	rwrFileName = argv._[2];

	src = fs.readFileSync ('/dev/fd/0', 'utf-8');

	_traceDepth = 0;
	if (argv.trace) {
	    _tracing = true;
	}

	let grammarText = fs.readFileSync (grammarFileName, 'utf-8');
	let rwr = fs.readFileSync (rwrFileName, 'utf-8');

	let ast = makeAST (grammarName, grammarText);
	let cst = patternMatch (src, ast);
	let emptyAsst = makeASST (ast)
	let asst = hangOperationOntoAsst (emptyAsst, "rwr", rwrFileName);

	let walked = processCST ("rwr", asst, cst)
	return walked;
	
    } catch (e) {
	console.error (e.message.trim ());
	process.exit (1);
    }
}

var result = main ()
console.log (result.trim ());
