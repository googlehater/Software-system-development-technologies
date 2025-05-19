from .strategy import PaymentStrategy


class PaymentType:
    def __init__(self, strategy: PaymentStrategy) -> None:
        self.strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy) -> None:
        self.strategy = strategy

    def pay(self, amount: float) -> str:
        return self.strategy.pay(amount)
