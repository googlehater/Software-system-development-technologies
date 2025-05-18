from patterns.state.concrete_states import (
    ProvingState,
    PaidState,
    ShippedState,
    OrderState
)



class StateFactory:
    @staticmethod
    def create(status_name: str):
        if status_name == "prooving":
            return ProvingState()
        elif status_name == "paid":
            return PaidState()
        elif status_name == "shipped":
            return ShippedState()
        raise ValueError(f"Unknown status: {status_name}")
    