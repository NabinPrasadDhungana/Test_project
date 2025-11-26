import random

comp = random.randint(0, 100)
print("Computer has chosen a number, try to guess it.")
count = 5

while True:
    while count != 0:
        user_input = int(input("Try to guess the number between 0 and 100 (including): "))
        count -= 1

        if user_input == comp:
            print("Hurray! You have guessed the correct number.")
            break

        elif user_input > comp:
            print("Too High!")
            print(f"You have {count} attempts left.")
        
        else:
            print("Too Low!")
            print(f"You have {count} attempts left.")

    if count == 0:
        print("The actual number was", comp)
        print("Better Luck next time!")
    choice = input("Do you want to play again (y/n): ")

    if choice == 'n':
        break
    else:
        count = 5
