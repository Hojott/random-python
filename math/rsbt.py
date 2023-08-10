#!/usr/bin/env python3
from typing import Self, Any, Callable

class Fraction():
    def __init__(self, numenator: int, deminator: int):
        self.numenator: int = numenator
        self.deminator: int = deminator

    @classmethod
    def from_string(cls, string: str) -> Self:
        string_split: list = string.split("/")
        numenator: int = int(string_split[0])
        deminator: int = int(string_split[1])
        return Fraction(numenator, deminator)

    def abs(self) -> Self:
        return Fraction(abs(self.numenator), abs(self.deminator))

    def __add__(self, other: Self) -> Self:
        return Fraction(self.numenator+other.numenator, self.deminator+other.deminator)

    def __sub__(self, other: Self) -> Self:
        return Fraction(self.numenator-other.numenator, self.deminator-other.deminator)

    def __repr__(self) -> str:
        return f"{self.numenator}/{self.deminator}"

class RSBT():
    def __init__(self, start_a, start_b, depth):
        self.a = start_a
        self.b = start_b
        self.depth = depth

    def simulate(self, sim_t: int) -> tuple[list[Fraction], list[list[Fraction]]]:
        match sim_t:
            case 0:
                print("Simulating standard SB-Tree")
                return self.sbt(self.rsbt_0)
            case 1:
                print("Simulating Reversed SB-Tree 1 (Negatives left as is)")
                return self.sbt(self.rsbt_1)
            case 2:
                print("Simulating Reversed SB-Tree 2 (Absolute values)")
                return self.sbt(self.rsbt_2)
            case 3:
                print("Simulating Reversed SB-Tree 3 (Absolute values on reduction)")
                return self.sbt(self.rsbt_3)
            case _:
                print("Invalid input")
                return []

    def sbt(self, operate: Callable) -> tuple[list[Fraction], list[list[Fraction]]]:
        """ Simulate a Stern Brocot Tree with self-defined startingpoints, depth and operator """
        listed: list = [self.a, self.b]
        cached: list = [self.a, self.b]
        tree: list = [[self.a, self.b]]

        for d in range(1, self.depth+1):
            print(f"Depth {d}", end="\r")
            tree.append([])
            for i in range(len(listed)-1):
                new: Fraction = operate(listed[i], listed[i+1])
                cached = cached[:i*2+1] + [new] + cached[i*2+1:]
                tree[-1].append(new)
            listed[:] = cached

        print()
        return listed, tree

    @classmethod
    def rsbt_0(cls, a: Fraction, b: Fraction) -> Fraction:
        return a + b

    @classmethod
    def rsbt_1(cls, a: Fraction, b: Fraction) -> Fraction:
        return a - b

    @classmethod
    def rsbt_2(cls, a: Fraction, b: Fraction) -> Fraction:
        return (a - b).abs()

    @classmethod
    def rsbt_3(cls, a: Fraction, b: Fraction) -> Fraction:
        ab: Fraction = a - b
        if ab.numenator < 0 and ab.deminator < 0:
            ab = ab.abs()
        return ab

def main():
    print("Stern Brocot Tree - reversed")
    sim_t: int = int(input("Simulation type [0-3]: "))
    start: list = input("Simulation start: [2 fractions] ").split()
    start_a: Fraction = Fraction.from_string(start[0])
    start_b: Fraction = Fraction.from_string(start[1])
    depth: int = int(input("Simulation depth: [1-] "))

    rsbt = RSBT(start_a, start_b, depth)
    sim, fancy = rsbt.simulate(sim_t)
    for row in fancy:
        print(" ".join(map(str, row)))

if __name__ == "__main__":
    main()
