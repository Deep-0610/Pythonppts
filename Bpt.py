import math
import datetime

def calculator():
    a = int(input("Enter first number: "))
    b = int(input("Enter second number: "))

    print("Sum:", a + b)
    print("Difference:", a - b)
    print("Product:", a * b)
    print("Square root of first number:", math.sqrt(a))


def show_date_time():
    now = datetime.datetime.now()
    print("Current Date & Time:", now)


def main():
    print("1. Calculator")
    print("2. Show Date & Time")

    choice = input("Enter choice: ")

    if choice == "1":
        calculator()
    elif choice == "2":
        show_date_time()
    else:
        print("Invalid choice 😬")


main()
