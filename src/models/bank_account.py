from decimal import Decimal, InvalidOperation


from src.models.transaction import Transaction
from src.models.transaction_history import TransactionHistory
from src.exceptions.account import AccountBlockedError, InsufficientBalanceError


MoneyInput = str | int | Decimal


class BankAccount:
    def __init__(
        self,
        account_number,
        owner,
        initial_balance: MoneyInput = 0,
        overdraft_limit: MoneyInput = 0,
    ):

        self._account_number = account_number
        self._owner = owner
        self._balance = self._validate_non_negative_amount(initial_balance)
        self._overdraft_limit = self._validate_non_negative_amount(overdraft_limit)
        self._history = TransactionHistory()
        self._blocked = False

    @property
    def account_number(self):
        return self._account_number

    @property
    def balance(self) -> Decimal:
        return self._balance

    @property
    def history(self):
        return self._history

    @property
    def overdraft_limit(self) -> Decimal:
        return self._overdraft_limit

    @property
    def owner(self):
        return self._owner

    # Transaction Operations

    def deposit(self, amount: MoneyInput, register_transaction=True):
        amount = self._validate_positive_amount(amount)
        self._balance += amount

        if register_transaction:
            self._register_transaction(
                transaction_type="deposit",
                amount=amount,
                description="Deposit completed.",
                balance_after=self._balance,
            )

    def transfer(self, destination_account, amount: MoneyInput):
        self._validate_account(destination_account)
        amount = self._validate_positive_amount(amount)

        self.withdraw(amount, register_transaction=False)
        destination_account.deposit(amount, register_transaction=False)

        self._register_transaction(
            transaction_type="transfer_out",
            amount=amount,
            description=f"Transfer sent to account {destination_account.account_number}.",
            balance_after=self._balance,
            source_account=self,
            destination_account=destination_account,
        )

        destination_account._register_transaction(
            transaction_type="transfer_in",
            amount=amount,
            description=f"Transfer received from account {self.account_number}.",
            balance_after=destination_account.balance,
            source_account=self,
            destination_account=destination_account,
        )

    def withdraw(self, amount: MoneyInput, register_transaction=True):
        if self._blocked:
            raise AccountBlockedError("Blocked accounts cannot withdraw.")

        amount = self._validate_positive_amount(amount)
        self._has_sufficient_balance(amount)
        self._balance -= amount

        if register_transaction:
            self._register_transaction(
                transaction_type="withdraw",
                amount=amount,
                description="Withdrawal completed.",
                balance_after=self._balance,
            )

    # Transaction Internals

    def _register_transaction(
        self,
        transaction_type,
        amount,
        description,
        balance_after,
        source_account=None,
        destination_account=None,
    ):
        transaction = Transaction(
            transaction_type=transaction_type,
            amount=amount,
            description=description,
            balance_after=balance_after,
            source_account=source_account,
            destination_account=destination_account,
        )

        self._history.add_transaction(transaction)

    # Account Validation

    def _has_sufficient_balance(self, amount):
        available_balance = self._balance + self._overdraft_limit

        if amount > available_balance:
            raise InsufficientBalanceError("Insufficient balance for this transaction.")

    def _normalize_money(self, amount: MoneyInput) -> Decimal:
        if isinstance(amount, bool) or not isinstance(amount, (str, int, Decimal)):
            raise TypeError("Amount must be a str, an int, or a Decimal.")

        if not isinstance(amount, Decimal):
            try:
                amount = Decimal(amount)
            except InvalidOperation as exc:
                raise ValueError("Amount must be a valid numeric value.") from exc

        if not amount.is_finite():
            raise ValueError("Amount must be a finite numeric value.")

        return amount

    def _validate_account(self, account):
        if not isinstance(account, BankAccount):
            raise TypeError("Account must be a BankAccount instance.")

        if account is self:
            raise ValueError("Cannot transfer to the same account.")

    def _validate_non_negative_amount(self, amount: MoneyInput) -> Decimal:
        amount = self._normalize_money(amount)

        if amount < 0:
            raise ValueError("Amount must be greater than or equal to zero.")

        return amount

    def _validate_positive_amount(self, amount: MoneyInput) -> Decimal:
        amount = self._normalize_money(amount)

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        return amount

    def block_account(self):
        self._blocked = True
