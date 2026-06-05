## Intructions

### LABELS

syntax: `<LABEL>:`

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

    # Keywords
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
    ACC     = 114
    IN      = 115
    OUT     = 116
    STACK   = 117
    SCREEN  = 118

    IDENT   = 201
    STRING  = 202
    NUMBER  = 203
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
    | "ADD" src nl
    | "SUB" src nl
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
nl ::= nl+
```

- [ ] print no deberia poder imprimir un valor proveniente de IN
- [ ] aunque innesario, lo logico seria que tambien se pueda imprimir un numero

pensandolo bien, voy a sacar print.

con respecto a si es logico algo como `MOV IN, OUT`, lo dejare al criterio del usuario (yo).
