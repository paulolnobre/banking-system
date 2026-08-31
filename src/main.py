from src.models.bank import Bank


def main():
    bank = Bank()

    customer_a = bank.register_customer(
        name="Ana Silva",
        cpf="000.000.000-00",
        email="ana.silva@example.com",
        phone="(00) 00000-0000",
    )

    customer_b = bank.register_customer(
        name="Bruno Costa",
        cpf="111.111.111-11",
        email="bruno.costa@example.com",
        phone="(11) 11111-1111",
    )

    account_a = bank.create_account(
        owner=customer_a,
        initial_balance=10_000,
        overdraft_limit=1_000,
    )

    account_b = bank.create_account(
        owner=customer_b,
        initial_balance=5_000,
        overdraft_limit=500,
    )

    account_a.deposit(1_000)
    account_a.withdraw(500)
    account_a.transfer(account_b, 600)

    print(
        f"{account_a.owner.name}: "
        f"R$ {account_a.balance:.2f}"
    )

    print(
        f"{account_b.owner.name}: "
        f"R$ {account_b.balance:.2f}"
    )

    print("\nCustomer A transaction history:")

    for transaction in account_a.history.transactions:
        print(
            transaction.transaction_type,
            transaction.amount,
            transaction.description,
            transaction.timestamp,
            f"Balance after: {transaction.balance_after:.2f}",
        )


if __name__ == "__main__":
    main()
