import mod

def main():
    x = int(input("Enter first number: "))
    y = int(input("Enter second number: "))

    print("Addition:", mod.add(x, y))
    print("Subtraction:", mod.sub(x, y))
    print("Square of first number:", mod.square(x))

main()
