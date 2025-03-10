from customers.customer import Customer
from products.product import Product
from customers.customer_transactions import CustomerTransaction
from products.product_transactions import ProductTransaction
from customers.branches import CustomerBranch
from database import Database

db = Database()

def menu():
    print("""---Company Search Engine Menu---\n
        1. Add a new customer\n
        2. Search for a customer\n
        3. Update customer information\n
        4. Add a new product\n
        5. Search for a product\n
        6. Update product information\n
        7. View a customer's transaction history\n
        8. View a product purchase history\n
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
            # User input for adding a new customer
            customer_type = input("Enter customer type (Individual/Company): ")
            if customer_type.lower() == "individual":
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                company_name = None
            else:
                first_name = None
                last_name = None
                company_name = input("Enter company name: ")
            email = input("Enter email: ")
            phone = input("Enter phone number: ")
            branch_id = input("Enter branch ID: ")
            
            customer.NewCustomer(customer_type, first_name, last_name, company_name, email, phone, branch_id)

        elif choice == "2":
            customer_id = input("Enter customer ID to search: ")
            customer.SearchCustomer(customer_id)

        elif choice == "3":
            customer_id = input("Enter customer ID to update: ")
            email = input("Enter new email (leave blank to keep current): ")
            phone = input("Enter new phone (leave blank to keep current): ")
            branch_id = input("Enter new branch ID (leave blank to keep current): ")
            
            customer.UpdateCustomer(customer_id, email, phone, branch_id)

        elif choice == "4":
            # User input for adding a new product
            product_name = input("Enter product name: ")
            category = input("Enter product category: ")
            price = float(input("Enter product price: "))
            stock_quantity = int(input("Enter stock quantity: "))

            product.NewProduct(product_name, category, price, stock_quantity)

        elif choice == "5":
            product_id = input("Enter product ID to search: ")
            product.SearchProduct(product_id)

        elif choice == "6":
            product_id = input("Enter product ID to update: ")
            price = input("Enter new price (leave blank to keep current): ")
            stock_quantity = input("Enter new stock quantity (leave blank to keep current): ")
            
            product.UpdateProduct(product_id, price, stock_quantity)

        elif choice == "7":
            customer_id = input("Enter customer ID to view purchase history: ")
            customer_transactions.CustomerPurchase(customer_id)

        elif choice == "8":
            product_id = input("Enter product ID to view purchase history: ")
            product_transactions.ProductPurchase(product_id)

        elif choice == "9":
            print("Exiting program...")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
