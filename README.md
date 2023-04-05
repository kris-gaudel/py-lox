# py-lox
A tree-walking Lox interpreter in Python - based on the book "Crafting Interpreters" by Robert Nystrom

# Why?
- Programming language implementations are interesting!
- Get better at OOP (the book uses Java already, but I don't know Java)
- Get better at Python

# Features
Py-lox is a fully-featured interpreter for the Lox programming language. The lox language is very similar to Java, with focus on object-oriented design. The Lox language has the following features:
- Variables (`var`)
- Conditionals (`if`, `else if`, `else`)
- Iteration (`for`, `while`)
- Functions (`fun`)
- Classes (`class`, `super`)
- Printing (`print`)
- Comments (`//`)

# Examples

Printing to output: 

```lox
print "Hello, world!";
```

Conditionals:

```lox
var a = 1;

if (a == 1) {
  print "1";
} else {
  print "not 1";
}
```

Loops:

```lox
var b = 1;

while (b < 5) {
  print b;
  b = b + 1;
}

for (var b = 1; b < 5; b = b + 1) {
  print b;
}
```

Functions:

```lox
fun say_hello(name) {
  return "Hello" + name + "!";
}
print say_hello("Kris");
```

Classes:
```lox
class Breakfast {
  init(meat, bread) {
    this.meat = meat;
    this.bread = bread;
  }
}

class Brunch < Breakfast {
  init(meat, bread, drink) {
    super.init(meat, bread);
    this.drink = drink;
  }
}
```
