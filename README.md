# Boson

This my own programming language. Lexer, parser and interpreter were written using python.

Boson has basic functionalities like,
  -> Arithmetic operations  (+, -, *, /, %, **(pow))
  -> Relational operations  (<, >, <=, >=, !=, ==)
  -> Logical operations  (and, or, not)
  -> Bitwise operations  (&, |, ^, ~)

Variables :

  -> The variables can be assigned using "assign" keyword.
     For example : assign a = 5

  -> The values of variables can be re-assigned using "$" symbol.
     For example : $a = 6

User input :

  -> The input from user can obtained by using input() function. For integer input we can use input_int() function.

Print :

  -> print function is used to print the output the console screen.
  -> print function has 2 parameters which are output and separator.
     For example : print("Hello", " ")
                   print("world", "") # which prints "Hello world"
  -> "nl" used in separator for new line.
     For example : print("Hello", "nl")
                   print("world", "nl") # which prints "world" in next line followed by "Hello" in previous linne. 

Lists :

  -> It supports basic functionalities like add an element, remove element, extend another list etc...
  -> Element of an list can be accessed using index value followed by "@" symbol.
     For example : assign l = [1, 2, 3, 4, 5]
                   print(l @ 0, "nl") # which returns the value of 0th index value i.e 1.
  -> Add an element to the list.
     1) Using append function.
        For example : append(l, 6) # which add 6 to the list l.
     2) Using "+" symbol.
        For example : l + 6 # same as append function.
  -> Remove an element from the list.
     1) Using pop function.
        For example : pop(l, 6) # which remove 6 from the list l.
     2) Using "-" symbol.
        For example : l - 6 # same as pop function.
  -> Extend an list to the another list.
     1) Using extend function.
        For example : extend(l1, l2) # which extend list l2 to the list l1.
     2) Using "*" symbol.
        For example : l1 * l2 # same as extend function.
  -> To find a length of the list use len function.
     For example : print(len(l), "nl") # which outputs the length of the list l.
  -> is_list() function returns true if the element passed to it is a list.

Strings :

  -> "+" is used to concat to strings.
     For example : print("Hello " + "world", "nl") # which outputs "Hello world".
  -> To embed the value of variable into the string use "{}"
     For example : assign num = 5
                   print("The number is : { num }", "nl") # which outputs "The number is : 5".
                   # if the variable is not declared then it prints the same i.e "The number is : { num }"
  -> is_str() function returns true if the element passed to it is a string.

For loop :

  -> for loop can be used to loop the block of statements for given number of times.
     For example : assign sum = 0
                   assign fact = 1
                   for i = 1 to 6 then
                    $fact = fact * i
                    $sum = sum + i
                   end
                   print(fact, ",")
                   print(sum, "nl") # loop runs from 1 to 5 and prints 15,120
  -> single statement can be used in for loop without new line.
     For example : for i = 1 to 6 then print(i, ",") # which prints 1,2,3,4,5
  -> step value can be used to jump values.
     For example : for i = 1 to 6 step 2 then print(i, ",") # which prints 1,3,5
  -> break and continue keywords also can be used.

While loop :

  -> while loop can be used to loop the block of statements for given number of times.
     For example : assign i = 0
                   while i < 6 then
                    $sum = sum + i
                    $i = i + 1
                   end
                   print(sum, "nl") # loop runs from 1 to 5 and prints 15
  -> break and continue keywords also can be used.

If statement :

  -> if used to run the block of statements if condition is true.
     For example : if 1 < 5 then
                    print("Hello", "nl") # which outputs Hello"
                   end
  -> elif can be used to check many conditions. Multiple elif can be used.
     For example : if 2 > 5 then
                    print("Hello", "nl")
                   elif 5 < 7 then
                    print("world", "nl") # which outputs "world"
  -> else can be used to run a block of code if the given conditions are false.
     For example : if 2 > 5 then
                    print("Hello", "nl")
                   else
                    print("world", "nl")
                   end # which outputs "world"

Functions :

  -> functions are be used to write a block of statements once and can be used it many number of times.
  -> func keyword is used to for function declaration. "->" is used for single line statement.
     For example : func sum(a, b) -> return a + b
                   sum(1,2) # which outputs 3
                   sum(3,4) # which outputs 7
  -> multi-line statements can be used in new line with end keyword.
     For example : func num(a, b)
                    print(a+b, ",")
                    print(a*b, "nl")
                   end
                   num(2,3) # which outputs 5,6
  -> anonymous also can be used and assign to a variable.
     For example : assign sum = func(a, b) -> return a + b
                   print(sum, "nl") # which outputs <anonymous function>
                   print(sum(1,2), "nl") # which outputs 3
  -> is_func() function returns true if the element passed to it is a function.