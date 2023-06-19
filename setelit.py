result = []
for twenty in range (20): # 370/20 = n. 20
    for fifty in range (8):
        if twenty*20 + fifty*50 == 370:
            result.append((twenty, fifty))
print(result)
