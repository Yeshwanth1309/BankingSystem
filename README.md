# Banking System

## Project Description
A simple console-based banking system built in Python that allows users to create accounts, log in, view account details, deposit money, withdraw money, and transfer money. The system uses file handling to store user data, account balances, and transaction logs persistently. Passwords are securely hashed using SHA-256 for better security.

## Features
- **Account Creation**: Create a new account with a unique account number and password.
- **User Authentication**: Login with account number and password.
- **Account Management**: View account details, including balance and name.
- **Transactions**:
  - Deposit money into the account.
  - Withdraw money from the account.
  - Transfer money to another account.
- **Transaction Logging**: All transactions (deposit, withdrawal, transfer) are logged in a transaction log file (`transactions.log`).
- **Persistent Storage**: All data (account details, transactions) is stored in text files (`accounts.txt` and `transactions.log`).

## How to Run the Project

1. **Clone the Repository**:
   Clone the repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/BankingSystem.git
