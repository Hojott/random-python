import numpy as np

# Luodaan aakkoset
aakkoset = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"

# Luodaan modulus
n = len(aakkoset)

# Lasketaan aakkosten indeksit
indeksit = np.arange(len(aakkoset))

# Tehdään siirros indekseille modulo n
siirros = 123   # <-- Joudut vaihtamaan tätä indeksia tehtävässä
muutetut_indeksit = (indeksit - siirros)%n

# Tulostetaan selväkielen aakkoset ja salakielen korvaavat aakkoset
print("Selväkieliaakkoset:", aakkoset)
print("Salakieliaakkoset :", "".join([aakkoset[i] for i in muutetut_indeksit]))
