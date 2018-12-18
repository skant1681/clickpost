
class InvalidDataException(Exception):

    def __init__(self,value,msg):
        self.value = value
        self.msg = msg

    # str is to print() the value
    def __str__(self):
        return repr(self.value)