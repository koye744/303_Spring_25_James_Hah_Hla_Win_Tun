import string
import datetime

def encode(input_text, shift):
    """Encodes a given text using the Cesar cipher.
    Converts the entire input to lowercase, then shifts each letter.
    Non-alphabetic characters are left unchanged.
    Returns a tuple containing the alphabet and the encoded text"""

    alphabet = list(string.ascii_lowercase)
    if input_text == "":
        return (alphabet, "")
     
    input_text = input_text.lower()
    result = ""

    for ch in input_text:
        if ch.isalpha() and ch.islower():
            index = ord(ch) - ord('a')
            new_index = (index + shift) % 26
            result += chr(new_index + ord('a'))
        elif ch.isalpha() and ch.isupper():
            index = ord(ch) - ord('A')
            new_index = (index + shift) % 26
            result += chr(new_index + ord('A'))
        else:
            result += ch

    return (alphabet, result)

def decode(input_text, shift):
    """Decodes a given text using the Cesar cipher."""
    decoded_text = ""

    for char in input_text:
        if char.isalpha():
            shift_base = ord ('A') if char.isupper() else ord('a')
            decoded_text += chr((ord(char) - shift_base - shift) % 26 + shift_base)
        else:
            decoded_text += char

    return decoded_text

class BankAccount:
    """Represents a bank account with basic deposit and withdraw functionalities."""
    def __init__(self, name="Rainy", ID="1234", creation_date=datetime.date.today(), balance=0):
        if creation_date > datetime.date.today():
            raise Exception("Future account creation date is not allowed.")
        self.name = name
        self.ID = ID
        self.creation_date = creation_date
        self.balance = balance

    def deposit(self, amount):
        """Deposits money into the account."""
        if amount < 0:
            print("Negative deposit not allowed.")
            return
        self.balance += amount
        print(f"New balance: ${self.balance}")

    def withdraw(self, amount):
        """Withdraws money from the account if there are sufficiente funds."""
        if self.balance - amount < 0:
            print("Insufficient funds.")
            return
        self.balance -= amount
        print(f"New balance: ${self.balance}")

    def view_balance(self):
            """Displays the current blance."""
            return self.balance
    
class SavingsAccount(BankAccount):
    """A savings account where withdrawals are not only allowed after 180 days."""
    def withdraw(self, amount):
        if (datetime.date.today() - self.creation_date).days < 180:
            print("Withdrawals are only allowed after 180 days.")
            return
        if self.balance - amount < 0:
            print("Insufficient funds.")
            return
        self.balance -= amount
        print(f"New balance: ${self.balance}")

class CheckingAccount(BankAccount):
    """A checking account that allows overdrafts with a $30 fee."""
    def withdraw(self, amount):
        if self.balance - amount < 0:
            self.balance -= (amount + 30)
        else:
            self.balance -= amount
        print(f"New balance: ${self.balance}")

        
        
           