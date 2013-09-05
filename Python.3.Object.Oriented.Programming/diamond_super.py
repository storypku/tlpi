class BaseClass:
    def __init__(self):
        self.num_base_calls = 0

    def call_me(self):
        print("Calling method on Base Class")
        self.num_base_calls += 1

class LeftSubclass(BaseClass):
    def __init__(self):
        super().__init__()
        self.num_left_calls = 0

    def call_me(self):
        super().call_me()
        print("Calling method on Left Subclass")
        self.num_left_calls += 1

class RightSubclass(BaseClass):
    def __init__(self):
        super().__init__()
        self.num_right_calls = 0

    def call_me(self):
        super().call_me()
        print("Calling method on Right Subclass")
        self.num_right_calls += 1

class SubClass(LeftSubclass, RightSubclass):
    def __init__(self):
        self.num_sub_calls = 0
        super().__init__()

    def call_me(self):
        super().call_me()
        print("Calling method on Subclass")
        self.num_sub_calls += 1
