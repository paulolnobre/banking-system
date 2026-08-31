from datetime import datetime


class Transaction:
    def __init__(
        self,
        transaction_type,
        amount,
        description,
        balance_after,
        source_account=None,
        destination_account=None,
    ):
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description
        self.balance_after = balance_after
        self.source_account = source_account
        self.destination_account = destination_account
        self.timestamp = datetime.now()
