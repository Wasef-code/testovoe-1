from typing import Any


class Conditioner:
    @staticmethod
    def AnyEqual(right: Any, *args) -> bool:
        for i in args:
            if i == right:
                return True
        return False

    @staticmethod
    def AllEqual(right: Any, *args) -> bool:
        for i in args:
            if i != right:
                return False
        return True

    @staticmethod
    def Any(*args):
        for i in args:
            if i:
                return True
        return False

    @staticmethod
    def All(*args):
        for i in args:
            if not i:
                return False
        return True
