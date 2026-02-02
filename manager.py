import json 
import os
from typing import List 
from expense import Expense # Import our class from phase 2 
from income import Income

class FinanceManager:
    def __init__(self, filename="data_store.json"):
        self.filename = filename 
        self.expenses: List[Expense] = [] # A list to hold our Expense objects
        self.paychecks: List[Income] = [] # A list to hold income objects 
        self.load_data() # Load existing data when the manager starts 

    def add_expense(self, amount: float, category: str, description: str, username: str):
        new_expense = Expense(amount, category, description, username)
        self.expenses.append(new_expense)
        self.save_data() # Save immediately after adding 
        print("Expense added successfully!")

    def add_income(self, amount: float, job: str, description: str, username: str):
        new_income = Income(amount, job, description, username)
        self.paychecks.append(new_income)
        self.save_data() # Save immediately after adding 
        print("Income added successfully!")


    def get_user_expenses(self, username: str) -> List[Expense]:
        return [e for e in self.expenses if e.owner == username]

    def get_user_paychecks(self, username: str) -> List[Income]:
        return [i for i in self.paychecks if i.owner == username]

    def get_total_spent(self) -> float:
        # A generator expression (efficient way to sum list items)
        return sum(e.amount for e in self.expenses)

    def get_total_earned(self) -> float:
        # A generator expression (efficient way to sum list items)
        return sum(i.amount for i in self.paychecks)


    def get_expenses_by_category(self) -> dict:
    # Grouping expenses {'Food': 50.0, 'Transport': 20.0}
        report = {}
        for e in self.expenses:
            if e.category not in report:
                report[e.category] = 0
            report[e.category] += e.amount 
        return report

    def get_paychecks_by_category(self) -> dict:
    # Grouping income {'Job': 50.0, 'Side hustle': 20.0}
        report = {}
        for i in self.paychecks:
            if i.job not in report:
                report[i.job] = 0
            report[i.job] += i.amount 
        return report

    def save_data(self):
        # Convert all Expense objects to dictionaries 
        data_to_save = [e.to_dict() for e in self.expenses]
        data_to_save += [i.to_dict() for i in self.paychecks]
        with open(self.filename, "w") as f:
            json.dump(data_to_save, f, indent=4)

    def load_data(self):
        if not os.path.exists(self.filename):
            return # File doesn't exist yet, nothing to load 
        try: 
            with open(self.filename, "r") as f:
                raw_data = json.load(f) 
                # Convert the loaded dictionaries back into Expense objects 
                self.expenses = [
                    Expense(item['amount'], item['category'], item['description'], item['date'])
                    for item in raw_data 
                ]
                self.paychecks = [
                    Income(item['amount'], item['job'], item['description'], item['date'])
                    for item in raw_data 
                ]
        except(json.JSONDecodeError, KeyError):
            print("Warning: Data file corrupted or empty. Starting fresh.")
            self.expenses = []
            self.paychecks = []

        self.expenses = [
            Expense(
                item['amount'],
                item['category'],
                item['description'],
                item.get('owner', 'admin'),
                item['date']
            )
            for item in raw_data
        ]
        
        #self.paychecks = [
        #    Income(
        #       item['amount'],
        #       item['job'],
        #       item['description'],
        #       item.get('owner', 'admin'),
        #       item['date']
        #   )
        #   for item in raw_data
        #]

