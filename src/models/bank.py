from src.exceptions.bank import AccountNotFoundError, CustomerNotFoundError
from src.models.bank_account import BankAccount
from src.models.customer import Customer



class Bank:
    def __init__(self):
        self._last_customer_id = 1000
        self._last_account_number = 1000

        self._customers = {}
        self._accounts = {}

    # Account Operations

    def create_account(self, owner, initial_balance=0, overdraft_limit=0):
        self._validate_registered_customer(owner)
        self._last_account_number += 1

        account_number = self._last_account_number

        account = BankAccount(
            account_number=account_number,
            owner=owner,
            initial_balance=initial_balance,
            overdraft_limit=overdraft_limit,
        )

        self._add_account(account)

        return account

    def get_account(self, account_number):
        if isinstance(account_number, bool) or not isinstance(account_number, int):
            raise TypeError("Account number must be an integer.")

        if account_number <= 0:
            raise ValueError("Account number must be a positive integer.")
        
        if account_number not in self._accounts:
            raise AccountNotFoundError("This account does not exist.")

        return self._accounts[account_number]

    def get_account_by_owner(self, owner):  
        accounts_by_owner = []

        for account in self._accounts.values():
            if account.owner is owner:
                accounts_by_owner.append(account)

        return accounts_by_owner

    def remove_account(self, account_number):
        account = self.get_account(account_number)

        if account.balance != 0:
            raise ValueError("Account must be empty.")

        del self._accounts[account_number]

    # Customer Operations

    def get_customer(self, customer_id):
        if isinstance(customer_id, bool) or not isinstance(customer_id, int):
            raise TypeError("Customer ID must a int.")

        if customer_id <= 0:
            raise ValueError("Customer ID must be a positive integer.")

        if customer_id not in self._customers:
            raise CustomerNotFoundError("Customer ID is not registered.")

        return self._customers[customer_id]

    def register_customer(
        self,
        name,
        cpf,
        email,
        phone,
    ):
        if self._customer_exists_by_cpf(cpf):
            raise ValueError("CPF already registered.")

        self._last_customer_id += 1
        customer_id = self._last_customer_id

        customer = Customer(
            customer_id=customer_id,
            name=name,
            cpf=cpf,
            email=email,
            phone=phone,
        )

        self._customers[customer.customer_id] = customer

        return customer

    def remove_customer(self, customer_id):
        customer = self.get_customer(customer_id)

        accounts = self.get_account_by_owner(customer)

        if accounts:
            raise ValueError("This customer still have accounts.")

        del self._customers[customer_id]

    # Account Internals

    def _add_account(self, account):
        if not isinstance(account, BankAccount):
            raise TypeError("Account must be a BankAccount instance.")

        if account.account_number in self._accounts:
            raise ValueError("Account already exists.")

        self._accounts[account.account_number] = account

    # Customer Validation

    def _customer_exists_by_cpf(self, cpf):
        for customer in self._customers.values():
            if customer.cpf == cpf:
                return True

        return False

    def _validate_registered_customer(self, owner):
        if not isinstance(owner, Customer):
            raise TypeError("Owner must be a Customer instance.")

        if owner.customer_id not in self._customers:
            raise ValueError("Owner must be registered in this bank.")

        registered_customer = self._customers.get(owner.customer_id)

        if registered_customer is not owner:
            raise ValueError("Owner does not match the registered customer.")
