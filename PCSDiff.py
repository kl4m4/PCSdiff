import PV_PCSDiffLib
import sys

if len(sys.argv) != 3:
    print(sys.argv)
    print("Sposób użycia:\nPCSDiff plik1 plik2")
    
pathA = sys.argv[1]
pathB = sys.argv[2]

print("Otwieram plik A: {0}".format(pathA))
try:
    pagesListA = PV_PCSDiffLib.getPagesListFromFile(pathA)
    if len(pagesListA) <= 0:
        print("Projekt jest pusty! Prawdopodobnie jakiś błąd formatu.")
        exit()
except IOError:
    print("Nie mogę otworzyć pliku!")
    exit()

print("Otwieram plik B: {0}".format(pathB))
try:
    pagesListB = PV_PCSDiffLib.getPagesListFromFile(pathB)
    if len(pagesListA) <= 0:
        print("Projekt jest pusty! Prawdopodobnie jakiś błąd formatu.")
        exit()
except IOError:
    print("Nie mogę otworzyć pliku!")
    exit()
    
diffs = PV_PCSDiffLib.getDifferencesByPageOrder(pagesListA, pagesListB)
if len(diffs) <= 0:
    print("Brak różnic")
    exit()

print('\n')

print('\t\t\tProjekt A\t\t\t\t\t\tProjekt B')

printformat = '{:3}|{:7}|{:27}|{:20}||{:7}|{:27}|{:20}'    
print(printformat.format('##','Strona', 'Tytuł', 'Data modyf.','Strona','Tytuł','Data modyf.'))
print('-----------------------------------------------------------------------------------------------------------------------')

for index in range(0,len(diffs)):
    print(printformat.format(diffs[index][0]+1, diffs[index][1], diffs[index][3][0:26], diffs[index][5], diffs[index][2], diffs[index][4][0:26], diffs[index][6]))