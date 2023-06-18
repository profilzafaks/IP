import csv

class Varijante:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.varijante = self.ucitaj_varijante()

    def ucitaj_varijante(self):
        varijante = []
        with open(self.csv_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                variant_id = row[0]
                gene = row[1]
                variation = row[2]
                bolest = row[13]
                consequence = row[12]
                varijante.append((variant_id, gene, variation, bolest, consequence))
        return varijante

    def izracunaj_postotak_bolesti(self, ime_bolesti):
        broj_povezanih = sum(1 for varijanta in self.varijante if varijanta[3] == ime_bolesti)
        ukupno = len(self.varijante)
        postotak = (broj_povezanih / ukupno) * 100
        return postotak

    def postotak_predvidenog_ucinka(self, ime_ucinka):
        broj_ucinaka = sum(1 for varijanta in self.varijante if varijanta[4] == ime_ucinka)
        ukupno = len(self.varijante)
        postotak = (broj_ucinaka / ukupno) * 100
        return postotak


# Primjer korištenja klase Varijanta
csv_file = 'gnomAD.csv'
varijante = Varijante(csv_file)

ime_bolesti = 'Benign'
postotak_bolesti = varijante.izracunaj_postotak_bolesti(ime_bolesti)
#print(f"Postotak varijanti povezanih s bolešću '{ime_bolesti}': {postotak_bolesti}%")

ime_ucinka = "missense_variant"
postotak_ucinka = varijante.postotak_predvidenog_ucinka(ime_ucinka)
#print(f"Postotak varijanti s povezanim učinkom '{ime_ucinka}': {postotak_ucinka}%")