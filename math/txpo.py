#!/usr/bin/env python3
import typing
import math

def main():
    start: int = int(input("Input start: "))
    rounds: int = int(input("Input rounds: "))
    results_i: list = []
    results_l: list = []
    for r in range(rounds):
        result: list = txpo(start + r, r)
        results_i.append(result[0])
        results_l.append(result[2])

    state: str = f"start: {start},\nrounds: {rounds}"
    best_results: str = f"most iterations: {max(results_i)}\nlargest number: {max(results_l)}"

    print(state)
    print(best_results)


def txpo(start: int, round: int = 0) -> list[int, int, int]:
    number: int = start
    largest: int = number
    i: int = 0
    
    if not round % 10000:
        print(f"r: {round}", end="\r")
    while number != 1:
        i += 1

        if not number % 2:
            number = number // 2
        else:
            number = number*3 + 1

        if number > largest:
            largest = number

        #data: str = f"i: {i},    \tn: {number},    \tl: {largest}, {math.floor(math.log10(start))*' '}\tr: {round}    "
        #print(data, end="      \r")

    #print(data)
    return [i, number, largest]

if __name__ == "__main__":
    main()
