import random

while True:
    comp = random.randint(0, 100)
    print("Computer has chosen a number, try to guess it.")
    count = 5
    while count != 0:
        try:
            user_input = int(input("Try to guess the number between 0 and 100 (including): "))
        except ValueError:
            print('Enter valid number only')
            continue

        count -= 1
        succeed = False

        if user_input == comp:
            print("Hurray! You have guessed the correct number.")
            succeed = True
            break

        elif user_input > comp:
            print("Too High!")
            print(f"You have {count} attempts left.")
        
        else:
            print("Too Low!")
            print(f"You have {count} attempts left.")

    if not succeed:
        print("The actual number was", comp)
        print("Better Luck next time!")
    choice = input("Do you want to play again (y/n): ").lower()

    if choice == 'n':
        break
