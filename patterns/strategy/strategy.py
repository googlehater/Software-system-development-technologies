from abc import ABC, abstractmethod


# абстрактная стратегия
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass


# конкретная стратегия: оплата картой 
class CardPayment(PaymentStrategy):
    def pay(self, amount: float) -> str:
        return f'Оплата по карте на сумму: {amount} руб.'
    

# конкретная стратегия: оплата в рассрочку
class InstallmentPlanPayment(PaymentStrategy):
    def pay(self, amount: float) -> str:
        return f'Оплата по рассрочке на сумму: {amount} руб.'


class CashByDelivery(PaymentStrategy):
    def pay(self, amount: float) -> str:
        return f'Оплата наличными при получении на сумму: {amount} руб.'
