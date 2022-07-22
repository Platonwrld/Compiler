# Simple Compiler Written in Python

This is simple compiler written in python that going to implement is a our own dialect of BASIC to C.
For instance:

code2

The code in the python compiler contain mostly OOP and contain my comments on classes and methods. I also tried to declare variables in a clear language.

photo tokens

Сompiler will follow a three step process that is illustrated below. First, given the inputted source code, it will break the code up into tokens. These are like words and punctuation in English. Second, it will parse the tokens to make sure they are in an order that is allowed in our language. Third, it will emit the C code that our language will translate to.

photo diagr

Used these three steps as the main organization for our code. The lexer, parser, and emitter will each have their own Python code file. 

When the code is written and saved like code.simp you should type in shell this:

    python3 main.py code.simp

Will be created file out.c that you can compile:

	gcc out.c


And you get:

photo

Great! This is code on C. Compiler work!