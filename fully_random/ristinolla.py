# Ristinolla

# Pelilauta on 3x3 ruudukko (eli lista jossa on kolme listaa)
pelilauta = [ 
             [ '-', '-', '-' ],
             [ '-', '-', '-' ],
             [ '-', '-', '-' ]
            ]

# Merkataan vuorot sillä, onko vuoro parillinen
vuoro = 0

säännöt = "Tervetuloa ristinollaan! Anna vastaukset muodossa YX, esimerkiksi 13 on yläoikea."
print(säännöt)

while True:

    # Jos parillinen
    if vuoro % 2 == 0:
        koordinaatit = input("Pelaaja X: ")
        
        # Laitetaan uusi merkki koordinaateille käyttämällä merkkijonoa listana
        pelilauta[int(koordinaatit[0])-1][int(koordinaatit[1])-1] = 'X'
    
    # Jos pariton
    else:
        koordinaatit = input("Pelaaja O: ")

        pelilauta[int(koordinaatit[0])-1][int(koordinaatit[1])-1] = 'O'

    # Tulostetaan lauta
    print(str(pelilauta[0]) + "\n" + str(pelilauta[1]) + "\n" + str(pelilauta[2]))
    
    # Vaihetaan vuoroa
    vuoro += 1

