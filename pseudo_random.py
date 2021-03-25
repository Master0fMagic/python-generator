

from typing import Iterable


class PseudoRandom:
    __A=1366
    __C=150889
    __M=714025

    @staticmethod
    def get_M() -> int:
        return PseudoRandom.__M

    @staticmethod
    def get_C() -> int:
        return PseudoRandom.__C

    @staticmethod
    def get_A() -> int:
        return PseudoRandom.__A

    @staticmethod
    def get_random(number:int) -> int:
        return (PseudoRandom.__A*number + PseudoRandom.__C) % PseudoRandom.__M

    @staticmethod
    def get_random_list(number:int, amount:int, step:int) -> Iterable[int]:
        result = []
        random_number = PseudoRandom.get_random(number)
        result.append(random_number)
        for _ in range(amount - 1):
            random_number = PseudoRandom.get_random_with_step(random_number,step)
            result.append(random_number)
        return result
    
    @staticmethod
    def get_random_with_step(number:int,  step:int) -> int:
        for j in range(step):
            number = PseudoRandom.get_random(number)
        return number

