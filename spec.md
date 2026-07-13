```
program ::= {statement}

statement ::=
	| nop nl
	| mov src "," dst nl
	| swp nl
	| sav nl
	| add src nl
	| sub src nl
	| neg nl
	| jmp ident nl
	| jez ident nl
	| jnz ident nl
	| jgz ident nl
	| jlz ident nl
	| jro src nl

	| ident ":"
	| push src nl
	| pop dst nl
	| read nl
	| write src nl
	| define ident "," number nl
	| call ident nl
	| ret nl

src ::= acc
    | nil
    | bp
    | sp
    | bp[src]
    | sp[src]
    | ident
    | number

dst ::= acc
    | nil
    | bp
    | sp
    | bp[src]
    | sp[src]

nl ::= nl+
```
