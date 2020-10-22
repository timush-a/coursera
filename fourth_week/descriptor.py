class Value():
    """
    Descriptor that returns the account balance including commission
    """
    def __get__(self, obj, obj_type):
        return int(self.new_amount)

    def __set__(self, obj, value):
        self.new_amount = amount - amount * obj.commission


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission
