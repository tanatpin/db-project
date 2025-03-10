from customers.customer import Customer
from products.product import Product


def menu():
    print("Welcome to your Search Engine! Select one of the options: \n"
    "1. Add a new customer\n"
    "2. Search for an existing customer and their info\n"
    "3. Update information about an existing customer\n"
    "4. Search for an existing product and its info\n"
    "5. View a customer's transaction history\n"
    "6. View a your company's transaction history\n"
    "7. Add a product\n"
    "8. Exit Program")


while True:
    menu()
    choice = int(input("Select an option (number) from the choices above: "))

    if choice == 7:
        print("Successfully exited program.")
        break