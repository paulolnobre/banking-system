import pytest


from decimal import Decimal


from src.exceptions.account import AccountBlockedError, InsufficientBalanceError
from src.models.bank_account import BankAccount


@pytest.mark.parametrize(
    "initial_balance, overdraft_limit, expected_balance, expected_overdraft_limit",
    [
        (100, 0, Decimal("100"), Decimal("0")),
        ("100.50", "500.25", Decimal("100.50"), Decimal("500.25")),
        (Decimal("200.75"), Decimal("300"), Decimal("200.75"), Decimal("300")),

    ],
)
def test_bank_account_initialization(
    initial_balance, overdraft_limit,
    expected_balance,
    expected_overdraft_limit
):
    account = BankAccount(
        "1001",
        "Test Owner",
        initial_balance=initial_balance,
        overdraft_limit=overdraft_limit,
    )

    assert account.balance == expected_balance
    assert isinstance(account.balance, Decimal)

    assert account.overdraft_limit == expected_overdraft_limit
    assert isinstance(account.overdraft_limit, Decimal)

@pytest.mark.parametrize(
    "initial_balance, overdraft_limit, expected_exception",
    [
        (-100, 0, ValueError),
        (100, -500, ValueError),
        (100.50, 0, TypeError),
        (100, 500.25, TypeError),
        (True, 0, TypeError),
        ("abc", 0, ValueError),
    ],
)
def test_bank_account_initialization_exceptions(
    initial_balance,
    overdraft_limit,
    expected_exception
):
    with pytest.raises(expected_exception):
        BankAccount(
            "1001",
            "Test Owner",
            initial_balance=initial_balance,
            overdraft_limit=overdraft_limit,
        )

def test_deposit_preserves_decimal_precision():
    account = BankAccount(
        "1001",
        "Test Owner",
        initial_balance=Decimal("0"),
    )

    account.deposit("0.1")
    account.deposit("0.2")

    assert account.balance == Decimal("0.3")
    assert isinstance(account.balance, Decimal)

def test_withdraw_preserves_decimal_precision():
    account = BankAccount(
        "1001",
        "Test Owner",
        initial_balance=Decimal("0.5"),
    )

    account.withdraw("0.3")
    account.withdraw("0.2")

    assert account.balance == Decimal("0.0")
    assert isinstance(account.balance, Decimal)

def test_transfer_preserves_decimal_precision():
    account_from = BankAccount(
        "1001",
        "Test Owner",
        initial_balance=Decimal("1.0"),
    )

    account_to = BankAccount(
        "1002",
        "Maria",
        initial_balance=Decimal("0.0"),
    )

    account_from.transfer(account_to, "0.3")
    account_from.transfer(account_to, "0.2")

    assert account_from.balance == Decimal("0.5")
    assert isinstance(account_from.balance, Decimal)
    assert account_to.balance == Decimal("0.5")
    assert isinstance(account_to.balance, Decimal)

@pytest.fixture
def account_with_balance():
    return BankAccount(
        "1001",
        "Test Owner",
        initial_balance=Decimal("10.0"),
    )

def test_deposit_transaction_stores_decimal_values(account_with_balance):

    account_with_balance.deposit("10.5")

    transaction = account_with_balance.history.transactions[-1]

    assert transaction.amount == Decimal("10.5")
    assert isinstance(transaction.amount, Decimal)

    assert transaction.balance_after == Decimal("20.5")
    assert isinstance(transaction.balance_after, Decimal)

def test_withdraw_transaction_stores_decimal_values(account_with_balance):
    account_with_balance.withdraw("5.5")

    transaction = account_with_balance.history.transactions[-1]

    assert transaction.amount == Decimal("5.5")
    assert isinstance(transaction.amount, Decimal)

    assert transaction.balance_after == Decimal("4.5")
    assert isinstance(transaction.balance_after, Decimal)

def test_transfer_transaction_stores_decimal_values():
    account_from = BankAccount(
        "1001",
        "Test Owner",
        initial_balance=Decimal("10.0"),
    )

    account_to = BankAccount(
        "1002",
        "Maria",
        initial_balance=Decimal("0.0"),
    )

    account_from.transfer(account_to, "4.5")

    transaction_from = account_from.history.transactions[-1]
    transaction_to = account_to.history.transactions[-1]

    assert transaction_from.amount == Decimal("4.5")
    assert isinstance(transaction_from.amount, Decimal)
    assert transaction_from.balance_after == Decimal("5.5")
    assert isinstance(transaction_from.balance_after, Decimal)

    assert transaction_to.amount == Decimal("4.5")
    assert isinstance(transaction_to.amount, Decimal)
    assert transaction_to.balance_after == Decimal("4.5")
    assert isinstance(transaction_to.balance_after, Decimal)

NON_FINITE_VALUES = [
    Decimal("NaN"),
    Decimal("Infinity"),
    Decimal("-Infinity"),
    "NaN",
    "Infinity",
    "-Infinity",
]

@pytest.mark.parametrize("invalid_amount", NON_FINITE_VALUES)
def test_bank_account_rejects_non_finite_decimal_values(invalid_amount):
    with pytest.raises(ValueError):
        BankAccount(
            "1001",
            "Test Owner",
            initial_balance=invalid_amount,
        )

@pytest.mark.parametrize("invalid_amount", NON_FINITE_VALUES)
def test_deposit_rejects_non_finite_amount_and_preserves_balance(account_with_balance, invalid_amount):
    account = account_with_balance

    with pytest.raises(ValueError):
        account.deposit(invalid_amount)

    assert account.balance == Decimal("10.0")

@pytest.mark.parametrize("invalid_amount", NON_FINITE_VALUES)
def test_withdraw_rejects_non_finite_amount_and_preserves_balance(account_with_balance, invalid_amount):
    account = account_with_balance

    with pytest.raises(ValueError):
        account.withdraw(invalid_amount)

    assert account.balance == Decimal("10.0")

@pytest.mark.parametrize("invalid_amount", NON_FINITE_VALUES)
def test_transfer_rejects_non_finite_amount_and_preserves_balance(invalid_amount):
    account_from = BankAccount(
        "1001",
        "Test Owner",
        initial_balance=Decimal("10.0"),
    )
    account_to = BankAccount(
        "1002",
        "Maria",
        initial_balance=Decimal("0.0"),
    )

    with pytest.raises(ValueError):
        account_from.transfer(account_to, invalid_amount)

    assert account_from.balance == Decimal("10.0")
    assert account_to.balance == Decimal("0.0")

def test_blocked_account_cannot_withdraw():
    account = BankAccount(
        "1001",
        "Test Owner",
        initial_balance=Decimal("100")
    )

    account.block_account()

    with pytest.raises(AccountBlockedError):
        account.withdraw(Decimal("20"))

    assert account.balance == Decimal("100")

def test_blocked_account_cannot_transfer_out():
    account_from = BankAccount(
        "1001",
        "Test Owner",
        initial_balance=Decimal("100")
    )
    account_to = BankAccount(
        "1002",
        "Maria",
        initial_balance=Decimal("50")
    )

    account_from.block_account()

    with pytest.raises(AccountBlockedError):
        account_from.transfer(account_to, Decimal("20"))

    assert account_from.balance == Decimal("100")
    assert account_to.balance == Decimal("50")

def test_blocked_account_can_deposit():
    account = BankAccount(
        "1001",
        "Test Owner",
        initial_balance=Decimal("100")
    )

    account.block_account()

    account.deposit(Decimal("50"))

    assert account.balance == Decimal("150")

def test_blocked_account_can_transfer_in():
    account_from = BankAccount(
        "1001",
        "Test Owner",
        initial_balance=Decimal("100")
    )
    account_to = BankAccount(
        "1002",
        "Maria",
        initial_balance=Decimal("50")
    )

    account_to.block_account()

    account_from.transfer(account_to, Decimal("20"))

    assert account_from.balance == Decimal("80")
    assert account_to.balance == Decimal("70")

def test_account_with_insufficient_balance_cannot_withdraw():
    account = BankAccount(
        "1001",
        "Test Owner",
        initial_balance=Decimal("50")
    )

    with pytest.raises(InsufficientBalanceError):
        account.withdraw(Decimal("100"))

    assert account.balance == Decimal("50")

def test_account_with_insufficient_balance_cannot_transfer_out():
    account_from = BankAccount(
        "1001",
        "Test Owner",
        initial_balance=Decimal("50")
    )
    account_to = BankAccount(
        "1002",
        "Maria",
        initial_balance=Decimal("0")
    )

    with pytest.raises(InsufficientBalanceError):
        account_from.transfer(account_to, Decimal("100"))

    assert account_from.balance == Decimal("50")
    assert account_to.balance == Decimal("0")

def test_blocked_account_with_insufficient_balance_raises_account_blocked_error():
    account = BankAccount(
        "1001",
        "Test Owner",
        initial_balance=Decimal("50")
    )

    account.block_account()

    with pytest.raises(AccountBlockedError):
        account.withdraw(Decimal("100"))

    assert account.balance == Decimal("50")