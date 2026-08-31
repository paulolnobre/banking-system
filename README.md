# Python Banking System

A small in-memory banking domain written in Python. The project is an object-oriented programming exercise centered on customers, accounts, transactions, validation, and automated tests.

## Features

- Register customers with validated name, CPF, email, and phone number data.
- Normalize CPF and phone number formatting before storing it.
- Prevent duplicate customer CPFs within a bank.
- Create sequential customer IDs and account numbers.
- Create accounts only for customers registered with the same `Bank` instance.
- Deposit, withdraw, and transfer funds between accounts.
- Support an optional overdraft limit for withdrawals and transfers.
- Keep the account balance read-only through properties.
- Record deposits, withdrawals, and both sides of transfers in transaction histories.
- Remove empty accounts and customers without remaining accounts.

## Project Structure

```text
banking-system-portfolio/
├── .github/
│   └── workflows/
│       └── tests.yml
├── .gitignore
├── README.md
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── exceptions/
│   │   ├── __init__.py
│   │   ├── account.py
│   │   ├── bank.py
│   │   └── customer.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── bank.py
│   │   ├── bank_account.py
│   │   ├── customer.py
│   │   ├── transaction.py
│   │   └── transaction_history.py
│   └── main.py
└── tests/
    ├── test_bank.py
    ├── test_bank_account.py
    └── test_customer.py
```

## Requirements

- Python 3
- `pytest` to run the test suite

Install the test dependency when needed:

```bash
python -m pip install pytest
```

## Run The Demo

From the project root:

```bash
python -m src.main
```

The demo creates two customers and accounts, performs a deposit, withdrawal, and transfer, then prints balances and transaction histories.

## Run Tests

```bash
python -m pytest -v
```

## Domain Model

### `Bank`

Acts as the aggregate manager for customers and accounts.

- `register_customer(name, cpf, email, phone)`
- `get_customer(customer_id)`
- `remove_customer(customer_id)`
- `create_account(owner, initial_balance=0, overdraft_limit=0)`
- `get_account(account_number)`
- `get_account_by_owner(owner)`
- `remove_account(account_number)`

Customer IDs and account numbers start at `1001` and are assigned sequentially. An account can be removed only when its balance is zero. A customer can be removed only when they have no accounts.

### `Customer`

Represents an account owner. Each customer has a `customer_id`, `name`, `cpf`, `email`, and `phone`. CPF values must contain exactly 11 digits after formatting is removed; phone numbers must contain 10 or 11 digits.

### `BankAccount`

Represents an account owned by a customer. Its public properties are `account_number`, `owner`, `balance`, `overdraft_limit`, and `history`.

- `deposit(amount)` adds a positive numeric amount.
- `withdraw(amount)` subtracts a positive numeric amount when it does not exceed the available balance plus overdraft limit.
- `transfer(destination_account, amount)` withdraws from the source, deposits into the destination, and records a transaction for each account.

Transfers to the same account are rejected. Boolean values are not accepted as monetary amounts.

### `Transaction` And `TransactionHistory`

Every completed account operation creates a `Transaction` with its type, amount, description, balance after the operation, related accounts when applicable, and timestamp. Each `BankAccount` owns a `TransactionHistory`, which stores transactions in its `transactions` list.

## Example

```python
from src.models.bank import Bank

bank = Bank()
customer = bank.register_customer(
    name="Ana Silva",
    cpf="000.000.000-00",
    email="ana.silva@example.com",
    phone="(00) 00000-0000",
)

account = bank.create_account(customer, initial_balance=100, overdraft_limit=50)
account.deposit(25)
account.withdraw(50)

print(account.balance)  # 75
```
