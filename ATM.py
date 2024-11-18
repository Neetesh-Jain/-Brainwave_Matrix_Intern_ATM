import os
import json

class ATM:
    MAX_LOAN_AMOUNT = 5000  # Maximum loan limit

    def __init__(self, data_file='accounts.json'):
        self.data_file = data_file
        self.current_user = None
        self.load_data()

    # Load user data from the JSON file
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.accounts = json.load(file)
        else:
            self.accounts = {}

    # Save user data to the JSON file
    def save_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.accounts, file, indent=4)

    # Create a new account
    def create_account(self):
        print("\n--- Create a New Account ---")
        username = input("Enter a username: ")
        if username in self.accounts:
            print("Username already exists. Please try another one.")
            return
        pin = input("Set a 4-digit PIN: ")
        self.accounts[username] = {
            'pin': pin,
            'balance': 0,
            'transactions': [],
            'loan': 0
        }
        self.save_data()
        print("Account created successfully!")

    # Authenticate a user with username and PIN
    def authenticate_user(self):
        print("\n--- User Login ---")
        username = input("Enter your username: ")
        pin = input("Enter your 4-digit PIN: ")
        user = self.accounts.get(username)
        
        if user and user['pin'] == pin:
            self.current_user = username
            print(f"Welcome, {username}!")
            return True
        else:
            print("Invalid username or PIN.")
            return False

    # Check current account balance
    def check_balance(self):
        balance = self.accounts[self.current_user]['balance']
        print(f"Your current balance is: ${balance}")

    # Deposit money into the account
    def deposit(self, amount):
        if amount > 0:
            self.accounts[self.current_user]['balance'] += amount
            self.accounts[self.current_user]['transactions'].append(f"Deposited: ${amount}")
            self.save_data()
            print(f"${amount} deposited successfully.")
        else:
            print("Deposit amount should be positive.")

    # Withdraw money from the account
    def withdraw(self, amount):
        if amount > 0:
            if amount <= self.accounts[self.current_user]['balance']:
                self.accounts[self.current_user]['balance'] -= amount
                self.accounts[self.current_user]['transactions'].append(f"Withdrew: ${amount}")
                self.save_data()
                print(f"${amount} withdrawn successfully.")
            else:
                print("Insufficient funds.")
        else:
            print("Withdrawal amount should be positive.")

    # View transaction history
    def view_transactions(self):
        transactions = self.accounts[self.current_user]['transactions']
        if transactions:
            print("\n--- Transaction History ---")
            for transaction in transactions:
                print(transaction)
        else:
            print("No transactions found.")

    # Request a loan
    def request_loan(self, amount):
        if amount > 0 and amount <= ATM.MAX_LOAN_AMOUNT:
            current_loan = self.accounts[self.current_user]['loan']
            if current_loan + amount <= ATM.MAX_LOAN_AMOUNT:
                self.accounts[self.current_user]['loan'] += amount
                self.accounts[self.current_user]['balance'] += amount
                self.accounts[self.current_user]['transactions'].append(f"Loan Granted: ${amount}")
                self.save_data()
                print(f"Loan of ${amount} granted successfully.")
            else:
                print("Loan request exceeds the maximum allowed limit.")
        else:
            print("Loan amount should be positive and within the limit.")

    # Repay an outstanding loan
    def repay_loan(self, amount):
        if amount > 0:
            loan = self.accounts[self.current_user]['loan']
            if loan > 0:
                if amount <= self.accounts[self.current_user]['balance']:
                    if amount <= loan:
                        self.accounts[self.current_user]['loan'] -= amount
                        self.accounts[self.current_user]['balance'] -= amount
                        self.accounts[self.current_user]['transactions'].append(f"Loan Repayment: ${amount}")
                        self.save_data()
                        print(f"Loan of ${amount} repaid successfully.")
                    else:
                        print(f"Amount exceeds the current loan balance of ${loan}.")
                else:
                    print("Insufficient balance to repay the loan.")
            else:
                print("You have no outstanding loans.")
        else:
            print("Repayment amount should be positive.")

    # View the current loan status
    def view_loan_status(self):
        loan = self.accounts[self.current_user]['loan']
        print(f"Current Loan Amount: ${loan}")

    # Main menu to interact with the ATM
    def run(self):
        while True:
            print("\n--- ATM Menu ---")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. View Transaction History")
            print("5. Request Loan")
            print("6. Repay Loan")
            print("7. View Loan Status")
            print("8. Logout")

            choice = input("Choose an option: ")

            if choice == '1':
                self.check_balance()
            elif choice == '2':
                amount = float(input("Enter deposit amount: "))
                self.deposit(amount)
            elif choice == '3':
                amount = float(input("Enter withdrawal amount: "))
                self.withdraw(amount)
            elif choice == '4':
                self.view_transactions()
            elif choice == '5':
                amount = float(input("Enter loan amount: "))
                self.request_loan(amount)
            elif choice == '6':
                amount = float(input("Enter repayment amount: "))
                self.repay_loan(amount)
            elif choice == '7':
                self.view_loan_status()
            elif choice == '8':
                print("Logging out...")
                self.current_user = None
                break
            else:
                print("Invalid option. Please choose a valid number.")

# Main program entry point
if __name__ == "__main__":
    atm = ATM()
    
    while True:
        print("\n--- Welcome to the ATM ---")
        print("1. Login")
        print("2. Create New Account")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            if atm.authenticate_user():
                atm.run()
        elif choice == '2':
            atm.create_account()
        elif choice == '3':
            print("Exiting... Thank you for using the ATM!")
            break
        else:
            print("Invalid choice. Please select a valid option.")
