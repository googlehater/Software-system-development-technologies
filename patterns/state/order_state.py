from __future__ import annotations
from abc import ABC, abstractmethod

class OrderState(ABC):
    @property
    @abstractmethod
    def name(self) -> str: 
        pass
    
    @abstractmethod
    def next(self, order: 'Order', session: 'Session'):
        pass
    
    @abstractmethod
    def prev(self, order: 'Order', session: 'Session'): 
        pass