contacts = {}

def add_contact(name, number):
    input_contact = {
        name: number,
    }
    if number in contacts.values():
        print("The same number already exists for another contact!")
        return
    
    contacts.update(input_contact)
    print(f"Contact added for {name}")

def remove_contact(name):
    if name in contacts:
        contacts.pop(name)
        print(f"Contact removed for {name}")
        
    else:
        print("Contact doesn't already exist!")

def update_contact():
    name = input("Enter name of the contact to update: ")
    if not name in contacts:
        print("The contact doesn't exist to update!")
        return
    
    else:
        number = input("Enter the number: ")
        contacts.update({name: number})
        print(f'Contact updated for {name}')

def view_contacts():
    print("All contacts are:")
    print(contacts)

while True:
    print("Select options:")
    print("1. Add contact   2. Remove contact")
    print("3. View contacts 4. Update contact")
    choice = input("Enter your choice (1/2/3/4): ")

    if choice in ['1', '2', '3', '4']:
        if choice == '1':
            name = input("Enter contact name: ")
            number = int(input("Enter contact number: "))
            add_contact(name, number)

        elif choice == '2':
            name = input("Enter name to remove: ")
            remove_contact(name)

        elif choice == '3':
            view_contacts()

        else:
            update_contact()

    else:
        print("Invalid option!")

    next_option = input("Do you want to continue operating (y/n): ")
    if next_option == 'n':
        break