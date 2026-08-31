import pytest


from src.models.bank import Bank
from src.exceptions.bank import AccountNotFoundError, CustomerNotFoundError


@pytest.fixture
def bank_with_customer():
    bank = Bank()

    customer = bank.register_customer(
        name="Test Customer",
        cpf="000.000.000-00",
        email="customer@example.com",
        phone="(00) 00000-0000",
    )

    return bank, customer


def test_remove_account_with_zero_balance(bank_with_customer):

    bank, customer = bank_with_customer

    account = bank.create_account(
        owner=customer,
        initial_balance=0,
        overdraft_limit=0,
    )

    bank.remove_account(account.account_number)

    with pytest.raises(AccountNotFoundError):
        bank.get_account(account.account_number)


@pytest.mark.parametrize(
    "initial_balance, overdraft_limit, withdraw_amount",
    [
        (100, 0, None),
        (0, 500, 100),
    ],
)


def test_remove_account_with_nonzero_balance(
    bank_with_customer,
    initial_balance,
    overdraft_limit,
    withdraw_amount,
):

    bank, customer = bank_with_customer

    account = bank.create_account(
        owner=customer,
        initial_balance=initial_balance,
        overdraft_limit=overdraft_limit
    )

    if withdraw_amount is not None:
        account.withdraw(withdraw_amount)

    with pytest.raises(ValueError):
        bank.remove_account(account.account_number)

    stored_account = bank.get_account(account.account_number)

    assert stored_account is account

def test_get_nonexistent_account_raises_account_not_found_error():
    bank = Bank()

    with pytest.raises(AccountNotFoundError):
        bank.get_account("nonexistent_account_number")

def test_get_nonexistent_customer_raises_customer_not_found_error():

    bank = Bank()

    with pytest.raises(CustomerNotFoundError):
        bank.get_customer(9999)

@pytest.mark.parametrize(
    "invalid_customer_id",
    [
        "invalid_customer_id",
        True,
        None,
        False,
        1.5,
    ],
)
def test_invalid_customer_id_type_raises_type_error(invalid_customer_id):
    bank = Bank()

    with pytest.raises(TypeError):
        bank.get_customer(invalid_customer_id)

@pytest.mark.parametrize(
    "invalid_customer_id",
    [
        0,
        -1,
        -999,
    ],
)
def test_non_positive_customer_id_raises_value_error(invalid_customer_id):
    bank = Bank()

    with pytest.raises(ValueError):
        bank.get_customer(invalid_customer_id)