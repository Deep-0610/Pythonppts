#!/usr/bin/env python3

# Import from the custom package
from pkg.subpkg1.mod1 import greet, add
from pkg.subpkg1.mod2 import farewell, multiply
from pkg.subpkg2.mod1 import hello, subtract
from pkg.subpkg2.mod2 import power, farewell as farewell2

# Import from Tsdd.py
from Tsdd import foo, Foo, s, a

def main():
    print("Welcome to the Python Package Demo!")

    # Use functions from subpkg1
    print(greet("Alice"))
    print(f"Addition: {add(10, 5)}")
    print(farewell("Bob"))
    print(f"Multiplication: {multiply(3, 4)}")

    # Use functions from subpkg2
    print(hello("Charlie"))
    print(f"Subtraction: {subtract(20, 7)}")
    print(farewell2("Dave"))
    print(f"Power: {power(2, 3)}")

    # Use from Tsdd.py
    print(f"Quote: {s}")
    print(f"List: {a}")
    foo("test")
    x = Foo()
    print(f"Foo instance: {x}")

if __name__ == '__main__':
    main()
