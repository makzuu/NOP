Interprete para un lenguaje de programacion, por ahora sin nomnbre, inspirado
en el lenguaje de programacion usado en el juego TIS-100.

## System Architecture

Solo existira un "nodo" de ejecucion, sin limite de lineas de codigo. A diferencia
del juego, al llegar a la ultima linea no se volvera a ejecutar la primera en
un loop infinito.

Los registers solo almacenan integers entre -999 y 999.

### ACC

Este register es usando como destino y fuente de operaciones como add, sub, jez,
etc.

### BAK

Este register se usa como el almacenamiento temporal de ACC y es accesible
solamente a traves de las instrucciones SAV y SWP.

## Instruction Set

### Comentarios

Todas las lineas que empiecen con el simbolo (#) son ignoradas.

### Labels

Labels son usadas como destino por instrucciones como JMP. Al ejecutar (JMP START),
la ejecucion se reanudara en la siguiente linea despues de el label START

Ejemplo:

```
LOOP:
JMP LOOP
```

Esto crearia un loop infinito.

### MOV

Syntax: `MOV <SRC>, <DST>`

Donde `<SRC>` es siempre un *INTEGER* y `<DST>` es siempre *ACC*.

El valor `<SRC>` es leido y escrito a `<DST>`.

### SWP

Los valores de *ACC* y *BAK* son intercambiados.

### SAV

El valor de *ACC* es copiado a *BAK*

### ADD

Syntax: `ADD <SRC>`

Donde `<SRC>` es un *Integer* o *ACC*.

Se suma el valor en *SRC* a *ACC* y el resultado se guarda en *ACC*.

### SUB

Syntax: `SUB <SRC>`

Donde `<SRC>` es un *Integer* o "ACC".

Se resta el valor en *SRC* a *ACC* y el resultado se guarda en *ACC*.

### NEG

El valor en *ACC* cambia de signo. No tiene efecto en el zero.

### JMP

Syntax: `JMP <LABEL>`

Reanuda la ejecucion en la instruccion siguiente a `<LABEL>`.

### JEZ

Syntax: `JEZ <LABEL>`

Salto condicional. Si el valor en *ACC* es igual a cero, resume la ejecucion
en la instruccion siguiente a `<LABEL>`.

### JNZ

Syntax: `JNZ <LABEL>`

Salto condicional. Si el valor en *ACC* es diferente de cero, resume la ejecucion
en la instruccion siguiente a `<LABEL>`.

### JGZ

Syntax: `JGZ <LABEL>`

Salto condicional. Si el valor en *ACC* es mayor a cero, resume ejecucion en la
instruccion siguiente a `<LABEL>`.

### JLZ

Syntax: `JLZ <LABEL>`

Salto condicional. Si el valor en *ACC* es menor a cero, resume ejecucion en la
instruccion siguiente a `<LABEL>`.

### JRO

...

### PRT

Syntax: `PRT <SRC>`

`<SRC>` puede ser una *STRING* (entre comillas), *ACC* o un *INTEGER*.

Escribe la `<SRC>` en la terminal.

### PSH

Syntax: `PSH <SRC>`

Donde `<SRC>` puede ser un *INTEGER* o *ACC*.

El valor de `<SRC>` es leido y puesto en la cima de la stack.

### POP

El valor en la cima del stack es consumido y escrito en *ACC*.

### DRW

...

### CLR

...

### WT

...

### CLL

...

### RTN 

...

### IN

...

## Ejemplos

Output numbers from 1 to 10.

```
MOV 1, ACC
LOOP:
SAV
SUB 11
JEZ DONE
SWP
PTR ACC
ADD 1
JMP LOOP
DONE:
```
