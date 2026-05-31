## Intructions

### LABELS

syntax: <LABEL>:

### MOV

syntax: `MOV <SRC>, <DST>`

### SWP

syntax: `SWP`

### SAV

syntax: `SAV`

### ADD

syntax: `ADD <SRC>`

### SUB

syntax: `SUB <SRC>`

### NEG

syntax: `NEG`

### JMP

syntax: `JMP <LABEL>`

### JEZ

syntax: `JEZ <LABEL>`

### JNZ

syntax: `JNZ <LABEL>`

### JGZ

syntax: `JGZ <LABEL>`

### JLZ

syntax: `JLZ <LABEL>`

### JRO

syntax: `JRO <SRC>`

## Tokens

```python
class TokenType(Enum):
    EOF     = -1
    NL      = 0
    COMMA   = 1
    COLON   = 2

    # Instructions
    MOV     = 101
    SWP     = 102
    SAV     = 103
    ADD     = 104
    SUB     = 105
    NEG     = 106
    JMP     = 107
    JEZ     = 108
    JNZ     = 109
    JGZ     = 110
    JLZ     = 111
    JRO     = 112
    PRINT   = 113

    IDENT   = 201
    STRING  = 202
    ACC     = 203
    IN      = 204
    OUT     = 205
    STACK   = 206
    SCREEN  = 207
```

## Grammar

- `{}`: zero or more.
- `[]`: zero or one.
- `+`: one or more of whatever is to the left.
- `()`: grouping.
- `|`: OR.


```
program ::= {statement}
statement ::= ident ":" nl
    | "MOV" src "," dst nl
    | "SWP" nl
    | "SAV" nl
    | "ADD" src "," dst nl
    | "SUB" src "," dst nl
    | "NEG" 
    | "JMP" ident nl
    | "JEZ" ident nl
    | "JNZ" ident nl
    | "JGZ" ident nl
    | "JLZ" ident nl
    | "JRO" src
    | "PRINT" readable | string
src ::= number | readable
dst ::= writable
readable ::= "ACC" | "IN" | "STACK"
writable ::= "ACC" | "OUT" | "STACK" | "SCREEN"
```
