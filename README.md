# Simple Compiler Written in Python

This is simple compiler written in the python that going to implement a own dialect of BASIC to C.
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

The code in the python compiler contains mostly OOP and aslo contains comments for classes and methods. I also tried to declare variables in a clear language.
```python
    # so that after the call main.py there was a file ['main.py ', 'code.simp']
    if len(sys.argv) != 2:
        sys.exit('Error: Compiler needs source file as argument.')

    # open the file with a code
    with open(sys.argv[1], 'r') as input_file:
        input = input_file.read()
```

Сompiler will follow a three step process that is illustrated below. First, given the inputted source code, it will break the code up into tokens. Second, it will parse the tokens to make sure they are in an order that is allowed in our language. Third, it will emit the C code that our language will translate to.

![](https://github.com/Platonwrld/Compiler/blob/main/src/picture.png)

When the code is written and saved for instance like code.simp you should type in a terminal this:

    python3 main.py code.simp

And you get C code in file out.c:

```c
#include <stdio.h>
int main(void){
float nums;
float a;
float b;
float c;
printf("Let's go to build compiler\n");
if(0 == scanf("%f", &nums)) {
nums = 0;
scanf("%*s");
}
a = 5;
b = 2;
while(nums>9){
printf("%.2f\n", (float)(a));
c = a+b;
a = b;
b = c;
nums = nums-1;
}
return 0;
}
```

Great! This is code on C. Compiler work! You can use any compiler for C code, gcc for example and your code will be work
