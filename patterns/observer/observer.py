from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    @abstractmethod
    def update(self, order_id: int, status: str):
        pass

    
class Subject(ABC):
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        # подписать наблюдателя
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        # отписать наблюдателя
        self._observers.remove(observer)

    def notify(self, order_id: int, status: str) -> None:
        # уведомить других наблюдателей
        for observer in self._observers:
            observer.update(order_id, status) 


# конкретный наблюдатель - email
class EmailNotification(Observer):
    def update(self, order_id, status) -> None:
        print(f'email: заказ {order_id} получил статус "{status}"')
    

# конкретный наблюдатель - номер телефона
class SMSNotification(Observer):
    def update(self, order_id, status) -> None:
        print(f'SMS: заказ {order_id} получил статус "{status}"')
