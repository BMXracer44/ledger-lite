from dataclasses import dataclass
from datetime import datetime 

@dataclass 
class Expense:
    amount: float 
    category: str 
    description: str
    owner: str # <--- Links expense to specific user 
    date: str = datetime.now().strftime("%Y-%m-%d")

    # A helper method to convert the objects into a dictionary 
    # We need this because JSON files only understand dictionaries, not Python Objects 
    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "owner": self.owner, 
            "date": self.date 
        }
