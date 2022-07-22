# Simple Compiler Written in Python

This is simple compiler written in python that going to implement is a own dialect of BASIC to C.
For instance:

```
PRINT "Let's go to build compiler"
INPUT strings

LET a = 5
LET b = 2

WHILE nums > 9 REPEAT
    PRINT a
    LET c = a + b
    LET a = b
    LET b = c
    LET nums = nums - 1
ENDWHILE
```

The code in the python compiler contains mostly OOP and aslo containw for comments on classes and methods. I also tried to declare variables in a clear language.
```
    # so that after the call main.py there was a file ['main.py ', 'code.simp']
    if len(sys.argv) != 2:
        sys.exit('Error: Compiler needs source file as argument.')

    # open the file with a code
    with open(sys.argv[1], 'r') as input_file:
        input = input_file.read()
```

Сompiler will follow a three step process that is illustrated below. First, given the inputted source code, it will break the code up into tokens. These are like words and punctuation in English. Second, it will parse the tokens to make sure they are in an order that is allowed in our language. Third, it will emit the C code that our language will translate to.

![](https://github.com/Platonwrld/Django-Shop/blob/main/screens/readygif.gif)

Used these three steps as the main organization for our code. The lexer, parser, and emitter will each have their own Python code file. 

When the code is written and saved like code.simp you should type in shell this:

    python3 main.py code.simp

Will be created file out.c that you can compile:

	gcc out.c


And you get:

photo

Great! This is code on C. Compiler work!