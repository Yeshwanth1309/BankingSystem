import os
import hashlib
from datetime import datetime

# Global file names
data_file = "accounts.txt"
transaction_log_file = "transactions.log"

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to initialize the file if it doesn't exist
def initialize_file():
    if not os.path.exists(data_file):
        with open(data_file, 'w') as f:
            f.write("")  # Create an empty file
    if not os.path.exists(transaction_log_file):
        with open(transaction_log_file, 'w') as f:
            f.write("")  # Create an empty transaction log file

# Function to create a new account
def create_account():
    print("\n--- Create New Account ---")
    name = input("Enter your name: ")
    account_number = input("Enter a unique account number: ")
    password = input("Set a password for your account: ")
    balance = 0  # Initial balance is zero

    # Check if account already exists
    if check_account_exists(account_number):
        print("Account with this number already exists. Try again!\n")
        return

    hashed_password = hash_password(password)

    # Save the account details to the file
    with open(data_file, 'a') as f:
        f.write(f"{account_number},{name},{hashed_password},{balance}\n")
    print("Account created successfully!\n")

# Function to check if an account exists
def check_account_exists(account_number):
    with open(data_file, 'r') as f:
        accounts = f.readlines()
        for account in accounts:
            details = account.strip().split(',')
            if details[0] == account_number:
                return True
    return False

# Function to login
def login():
    print("\n--- Login ---")
    account_number = input("Enter your account number: ")
    password = input("Enter your password: ")

    with open(data_file, 'r') as f:
        accounts = f.readlines()
        for account in accounts:
            details = account.strip().split(',')
            if details[0] == account_number:
                if details[2] == hash_password(password):
                    print("Login successful!\n")
                    return account_number
                else:
                    print("Incorrect password!\n")
                    return None
    print("Account not found!\n")
    return None

# Function to view account details
def view_account(account_number):
    print("\n--- View Account Details ---")

    with open(data_file, 'r') as f:
        accounts = f.readlines()
        for account in accounts:
            details = account.strip().split(',')
            if details[0] == account_number:
                print(f"Account Number: {details[0]}\nName: {details[1]}\nBalance: {details[3]}\n")
                return
    print("Account not found!\n")

# Function to deposit money
def deposit_money(account_number):
    print("\n--- Deposit Money ---")
    amount = float(input("Enter amount to deposit: "))

    with open(data_file, 'r') as f:
        accounts = f.readlines()

    updated_accounts = []
    account_found = False

    for account in accounts:
        details = account.strip().split(',')
        if details[0] == account_number:
            new_balance = float(details[3]) + amount
            updated_accounts.append(f"{details[0]},{details[1]},{details[2]},{new_balance}\n")
            account_found = True
            log_transaction(account_number, "Deposit", amount, new_balance)
        else:
            updated_accounts.append(account)

    if not account_found:
        print("Account not found!\n")
        return

    with open(data_file, 'w') as f:
        f.writelines(updated_accounts)

    print("Amount deposited successfully!\n")

# Function to withdraw money
def withdraw_money(account_number):
    print("\n--- Withdraw Money ---")
    amount = float(input("Enter amount to withdraw: "))

    with open(data_file, 'r') as f:
        accounts = f.readlines()

    updated_accounts = []
    account_found = False

    for account in accounts:
        details = account.strip().split(',')
        if details[0] == account_number:
            if float(details[3]) >= amount:
                new_balance = float(details[3]) - amount
                updated_accounts.append(f"{details[0]},{details[1]},{details[2]},{new_balance}\n")
                account_found = True
                log_transaction(account_number, "Withdraw", amount, new_balance)
            else:
                print("Insufficient balance!\n")
                return
        else:
            updated_accounts.append(account)

    if not account_found:
        print("Account not found!\n")
        return

    with open(data_file, 'w') as f:
        f.writelines(updated_accounts)

    print("Amount withdrawn successfully!\n")

# Function to transfer money to another account
def transfer_money(account_number):
    print("\n--- Transfer Money ---")
    target_account_number = input("Enter the target account number: ")

    # Check if target account exists
    if not check_account_exists(target_account_number):
        print("Target account not found!\n")
        return

    amount = float(input("Enter amount to transfer: "))

    with open(data_file, 'r') as f:
        accounts = f.readlines()

    updated_accounts = []
    sender_found = False
    recipient_found = False

    for account in accounts:
        details = account.strip().split(',')
        if details[0] == account_number:
            if float(details[3]) >= amount:
                new_balance = float(details[3]) - amount
                updated_accounts.append(f"{details[0]},{details[1]},{details[2]},{new_balance}\n")
                sender_found = True
                log_transaction(account_number, "Transfer Out", amount, new_balance)
            else:
                print("Insufficient balance!\n")
                return
        elif details[0] == target_account_number:
            new_balance = float(details[3]) + amount
            updated_accounts.append(f"{details[0]},{details[1]},{details[2]},{new_balance}\n")
            recipient_found = True

        else:
            updated_accounts.append(account)

    if not sender_found:
        print("Sender account not found!\n")
        return

    if not recipient_found:
        print("Recipient account not found!\n")
        return

    with open(data_file, 'w') as f:
        f.writelines(updated_accounts)

    print("Amount transferred successfully!\n")

# Function to log transaction history
def log_transaction(account_number, transaction_type, amount, new_balance):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(transaction_log_file, 'a') as f:
        f.write(f"{timestamp} - Account: {account_number}, Type: {transaction_type}, Amount: {amount}, New Balance: {new_balance}\n")

# Main menu
def main_menu():
    initialize_file()

    while True:
        print("\n--- Banking System Menu ---")
        print("1. Login")
        print("2. Create New Account")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            account_number = login()
            if account_number:
                user_menu(account_number)
        elif choice == '2':
            create_account()
        elif choice == '3':
            print("Exiting... Thank you for using the Banking System!\n")
            break
        else:
            print("Invalid choice! Please try again.\n")

# User menu after login
def user_menu(account_number):
    while True:
        print("\n--- User Menu ---")
        print("1. View Account Details")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Logout")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            view_account(account_number)
        elif choice == '2':
            deposit_money(account_number)
        elif choice == '3':
            withdraw_money(account_number)
        elif choice == '4':
            transfer_money(account_number)
        elif choice == '5':
            print("Logging out...\n")
            break
        else:
            print("Invalid choice! Please try again.\n")

if __name__ == "__main__":
    main_menu()
