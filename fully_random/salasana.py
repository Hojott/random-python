import random
def luo_salasana(pituus: int) -> str:
	return "".join([random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(pituus)])

print(luo_salasana(8))
