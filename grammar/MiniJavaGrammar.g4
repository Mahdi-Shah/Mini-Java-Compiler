grammar MiniJavaGrammar;

startRule: mainClass classDeclaration*;

mainClass: 'class' identifier '{' mainMethod '}';

mainMethod: 'public' 'static' 'void' 'main' '(' 'String' ('[' ']'|'...') identifier ')' '{'statement+ '}';

classDeclaration: 'class' identifier '{' fieldDeclaration* methodDeclaration* '}';

parameter: type identifier;

fieldDeclaration: type identifier  SC;

localDeclaration: type identifier SC;

methodDeclaration: 'public'? (type|'void') identifier '(' parameterList? ')' '{' methodBody '}';

parameterList: parameter(',' parameter)*;

methodBody: localDeclaration* statement* (returnStatement)?;

type: 'int' '['']'| 'boolean'| 'int' | 'char' | 'String' | identifier;

identifier: Identifier;

statement
:
	  nestedStatement
	| ifElseStatement
	| whileStatement
	| doWhileStatement
	| printStatement
	| variableAssignmentStatement
	| arrayAssignmentStatement
	| continueStatement
	| breakStatement
	| returnStatement
	| methodCallStatement
;

doWhileStatement: 'do' statement 'while' LP expression RP SC;

breakStatement: 'break' SC;

continueStatement: 'continue' SC;

arrayAssignmentStatement: identifier LSB expression RSB EQ expression SC;

variableAssignmentStatement: identifier EQ expression SC;

printStatement: 'System.out.println' LP expression RP SC;

whileStatement: 'while' LP expression RP statement;

ifElseStatement: 'if' LP expression RP statement ('else' statement)?;

nestedStatement: '{' statement* '}';

returnStatement: 'return' expression SC ;

methodCallStatement: expression SC;


expression
:
    expression LSB expression RSB                       # arrayAccessExpression
	| expression '.length'                              # dotlengthExpression
	| expression '.charAt' '(' expression')'            # dotcharatExpression
	| expression '.' identifier                         # fieldAccessExpression
	| expression ('.' identifier methodCallParams)+     # methodCallExpression
	| 'new' identifier '(' ')'                          # objectInstantiationExpression
    | 'new' type LSB expression RSB                     # arrayInstantiationExpression
	| expression TIMES expression                       # mulExpression
	| expression DIV expression                         # divExpression
	| expression PLUS expression                        # addExpression
	| expression MINUS expression                       # subExpression
	| expression LT(EQ)? expression                     # lessThanExpression
	| expression GT(EQ)? expression                     # greaterThanExpression
	| expression (EQ|NOT) EQ expression                 # equalityExpression
	| expression AND expression                         # andExpression
	| expression OR expression                          # orExpression
	| NOT expression                                    # notExpression
	|'this'                                             # thisExpression
	| '(' expression ')'                                # parenthesesExpression
	| STRING                                            # stringExpression
	| CHAR                                              # characterExpression
	| ('+'|'-')? IntegerLiteral                         # integerLitExpression
	| ('+'|'-')? identifier                             # identifierExpression
	| BooleanLiteral                                    # boolLitExpression
;

methodCallParams: '('(expression(',' expression)*)? ')' ;

DIV:'/';

OR:'||';

GT:'>';

AND:'&&';

LT:'<';

PLUS:'+';

MINUS:'-';

TIMES:'*';

NOT:'!';

LSB:'[';

RSB:']';

LP:'(';

RP:')';

RETURN:'return';

EQ:'=';

BooleanLiteral:'true'| 'false';

SC:';';

Identifier:JavaLetter JavaLetterOrDigit*;

WS: [ \r\t\n]+ -> skip ;

MULTILINE_COMMENT: '/*' .*? '*/' -> skip ;

LINE_COMMENT: '//' .*? '\n' -> skip ;

STRING:	'"'(ESC_SEQ| ~( '\\' | '"' ))* '"' ;

CHAR: '\''(ESC_SEQ| ~( '\'' | '\\' )) '\'' ;

IntegerLiteral: DecimalIntegerLiteral ;

fragment JavaLetter : [a-zA-Z$_] ; /* these are the 'java letters' below 0xFF*/

fragment JavaLetterOrDigit:[a-zA-Z0-9$_] ;/* these are the 'java letters or digits' below 0xFF */

fragment DecimalIntegerLiteral: DecimalNumeral IntegertypeSuffix? ;

fragment IntegertypeSuffix: [lL] ;

fragment DecimalNumeral: '0' | NonZeroDigit (Digits?| Underscores Digits) ;

fragment Digits: Digit (DigitsAndUnderscores? Digit)? ;

fragment Digit:'0'| NonZeroDigit ;

fragment NonZeroDigit:[1-9] ;

fragment DigitsAndUnderscores: DigitOrUnderscore+ ;

fragment DigitOrUnderscore: Digit| '_' ;

fragment Underscores: '_'+ ;

fragment HEX_DIGIT:	(	'0' .. '9'| 'a' .. 'f'| 'A' .. 'F') ;

fragment ESC_SEQ: '\\'('b'| 't'| 'n'| 'f'| 'r'| '"'| '\''| '\\')| UNICODE_ESC| OCTAL_ESC ;

fragment OCTAL_ESC: '\\'('0' .. '3')('0' .. '7')('0' .. '7') | '\\'('0' .. '7')('0' .. '7') | '\\'('0' .. '7') ;

fragment UNICODE_ESC: '\\' 'u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT ;