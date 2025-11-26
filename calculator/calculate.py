def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def divide(a, b):
    return a / b

def multiply(a, b):
    return a * b

def power(a, b):
    return a ** b

def root(a, b):
    return a ** (1/b)

while True:
    print("1. Add       2. Subtract")
    print("3. Multiply  4. Divide")
    print("5. Power     6. Root")
    user_input = input("Enter what you want to do: (1/2/3/4/5/6)")

    if user_input in ['1', '2', '3', '4', '5', '6']:
        a = float(input("Enter the first number: "))
        b = float(input("Enter the second number: "))

        if user_input == '1':
            print(f"Sum of {a} and {b} is ", add(a, b))

        elif user_input == '2':
            print(f"Subtraction of {a} and {b} is ", subtract(a, b))

        elif user_input == '3':
            print(f"Multiplication of {a} and {b} is ", multiply(a, b))

        elif user_input == '4':
            print(f"Division of {a} and {b} is ", divide(a, b))

        elif user_input == '5':
            print(f"Power of {a} and {b} is ", power(a, b))

        else:
            print(f"Root of {a} and {b} is ", root(a, b))
        
        choice = input("Do you want to continue? (y/n): ")
        if choice == 'n':
            break
    else:
        print("Invalid input!")
        