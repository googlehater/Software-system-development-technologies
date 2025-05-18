from __future__ import annotations
from abc import ABC, abstractmethod

class OrderState(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...
    
    @abstractmethod
    def next(self, order: 'Order', session: 'Session'): ...
    
    @abstractmethod
    def prev(self, order: 'Order', session: 'Session'): ...