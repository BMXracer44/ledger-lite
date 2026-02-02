from manager import FinanceManager

def print_menu():
    print("\n--- LedgerLite Finance Tracker ---")
    print("1. Add Expense")
    print("2. Add Income")
    print("3. View Total Balance")
    print("4. View Report by Category")
    print("5. Exit")

def main():
    manager = FinanceManager() 

    while True:
        manager.load_data 
        print_menu()
        choice = input("Select an option (1-4): ")

        if choice == "1":
            try:
                amt = float(input("Enter amount: "))
                cat = input("Enter category (Food, Rent, Fun): ")
                desc = input("Enter description: ")
                manager.add_expense(amt, cat, desc)
            except ValueError:
                print("Error: Please enter a valid number for amount.")

        elif choice == "2":
            try:
                amt = float(input("Enter amount: "))
                job = input("Enter job (Work, side hustle): ")
                desc = input("Enter description: ")
                manager.add_expense(amt, job, desc)
            except ValueError:
                print("Error: Please enter a valid number for amount.")


        elif choice == "3":
            total = manager.get_total_spent() 
            print(f"\nTotal Spent: ${total:.2f}")
        
        elif choice == "4":
            report = manager.get_expenses_by_category() 
            print("\nSpending by Category: ")
            for category, total in report.items():
                print(f" -{category}: ${total:.2f}")
        
        elif choice == "5":
            print("Goodbye! Data saved.")
            break 

        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
