
class Value:

    def __init__(self):
        self.value = 0

    def __get__(self, obj, obj_type):
        return self.value

    def __set__(self, obj, val):
        self.value = (1 - obj.commission) * self.value