class TransactionHistory:
    def __init__(self):
        self.transactions = []

    # Transaction Operations

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
