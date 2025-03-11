from customers.customer import Customer
from products.product import Product
from customers.customer_transactions import CustomerTransaction
from products.product_transactions import ProductTransaction
from customers.branches import CustomerBranch
from database import Database

db = Database()

def menu():
    print("""\n--- Company Search Engine Menu ---\n
        1. Add a new customer
        2. Search for a customer
        3. Update customer information
        4. Add a new product
        5. Search for a product
        6. Update product information
        7. View a customer's transaction history
        8. View a product purchase history
        9. Exit
    """)


def main():
    customer = Customer(db)
    product = Product(db)
    customer_transactions = CustomerTransaction(db)
    product_transactions = ProductTransaction(db)
    branches = CustomerBranch(db)

    while True:
        menu()
        
        choice = input("Enter your choice: ")

        if choice == "1":
            # Add a new customer
            customer_type = input("Enter customer type (Individual/Company): ").strip().lower()
            if customer_type == "individual":
                first_name = input("Enter first name: ").strip() or None
                last_name = input("Enter last name: ").strip() or None
                company_name = None
            elif customer_type == "company":
                first_name, last_name = None, None
                company_name = input("Enter company name: ").strip() or None
            else:
                print("Invalid customer type. Please enter 'Individual' or 'Company'.")
                continue

            email = input("Enter email: ").strip() or None
            phone = input("Enter phone number: ").strip() or None
            branch_id = input("Enter branch ID: ").strip()
            branch_id = int(branch_id) if branch_id.isdigit() else None

            customer.new_customer(customer_type, first_name, last_name, company_name, email, phone, branch_id)

        elif choice == "2":
            search_term = input("Enter customer name, company, or email to search: ").strip()
            customer.search_customer(search_term)

        elif choice == "3":
            customer_id = input("Enter customer ID to update: ").strip()
            email = input("Enter new email (leave blank to keep current): ").strip() or None
            phone = input("Enter new phone (leave blank to keep current): ").strip() or None
            branch_id = input("Enter new branch ID (leave blank to keep current): ").strip()
            branch_id = int(branch_id) if branch_id.isdigit() else None

            customer.update_customer(customer_id, email=email, phone_number=phone, branch_id=branch_id)

        elif choice == "4":
            # Add a new product
            product_name = input("Enter product name: ").strip()
            category = input("Enter product category: ").strip()
            price = input("Enter product price: ").strip()
            stock_quantity = input("Enter stock quantity: ").strip()

            try:
                price = float(price)
                stock_quantity = int(stock_quantity)
                product.new_product(product_name, category, price, stock_quantity)
            except ValueError:
                print("Invalid input for price or stock quantity. Please enter numerical values.")

        elif choice == "5":
            search_term = input("Enter product name or category to search: ").strip()
            product.search_product(search_term)

        elif choice == "6":
            product_id = input("Enter product ID to update: ").strip()
            price = input("Enter new price (leave blank to keep current): ").strip()
            stock_quantity = input("Enter new stock quantity (leave blank to keep current): ").strip()

            price = float(price) if price else None
            stock_quantity = int(stock_quantity) if stock_quantity else None

            product.update_product(product_id, price=price, stock_quantity=stock_quantity)

        elif choice == "7":
            customer_id = input("Enter customer ID to view purchase history: ").strip()
            customer_transactions.customer_purchase(customer_id)

        elif choice == "8":
            product_id = input("Enter product ID to view purchase history: ").strip()
            product_transactions.product_purchase(product_id)

        elif choice == "9":
            print("Exiting program...")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
