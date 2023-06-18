import random

class Geni:
    def __init__(self, nukleotidi):
        self.nukleotidi = nukleotidi

    def __str__(self):
        return self.nukleotidi
    
    def __add__(self, x):
        if not isinstance(x, Geni) and x!=0:
            assert False, 'Razliciti tipovi podataka'
        if x==0:
            return self
        novi = self.nukleotidi + x.nukleotidi
        return Geni(novi)
    
    def __radd__(self, x):
        if not isinstance(x, Geni) and x!=0:
            assert False, 'Razliciti tipovi podataka' 
        if x==0:
            return self
        novi = self.nukleotidi + x.nukleotidi
        return Geni(novi)
    
    def __invert__(self):
        pozicija = random.randint(0,len(self.nukleotidi))
        lista = ['A', 'T', 'C', 'G']
        mutacija = random.choice(lista)
        nukl = ''
        i=0
        for zn in self.nukleotidi:
            if i==pozicija:
                nukl = nukl + mutacija
            else:
                nukl = nukl + zn
            i = i + 1
        self.nukleotidi = nukl

    def __mod__(self, drugi_gen):
        if not isinstance(drugi_gen, Geni) and drugi_gen!=0:
            assert False, 'Razliciti tipovi podataka'
        if drugi_gen==0:
            return self
        duljina = min(len(self.nukleotidi), len(drugi_gen.nukleotidi))
        podudaranja = sum(1 for x, y in zip(self.nukleotidi, drugi_gen.nukleotidi) if x == y)
        try:
            postotak_podudaranja = (podudaranja / duljina) * 100
        except ZeroDivisionError:
            return 0
        return postotak_podudaranja

    def spoji_gene(self, drugi_gen):
        novi_gen = self.nukleotidi + drugi_gen.nukleotidi
        return Geni(novi_gen)

    def dodaj_mutaciju(self, mutacija):
        pozicija = random.randint(0,len(self.nukleotidi))
        lista = ['A', 'T', 'C', 'G']
        mutacija = random.choice(lista)
        nukl = ''
        i=0
        for zn in self.nukleotidi:
            if i==pozicija:
                nukl = nukl + mutacija
            else:
                nukl = nukl + zn
            i = i + 1
        self.nukleotidi = nukl

    def dodaj_mutaciju_dva(self):
        novi_Gen = Geni("")
        pozicija = random.randint(0,len(self.nukleotidi))
        lista = ['A', 'T', 'C', 'G']
        mutacija = random.choice(lista)
        nukl = ''
        i=0
        for zn in self.nukleotidi:
            if i==pozicija:
                nukl = nukl + mutacija
            else:
                nukl = nukl + zn
            i = i + 1
        novi_Gen.nukleotidi = nukl
        return novi_Gen

    def usporedi_gene(self, drugi_gen):
        duljina = min(len(self.nukleotidi), len(drugi_gen.nukleotidi))
        podudaranja = sum(1 for x, y in zip(self.nukleotidi, drugi_gen.nukleotidi) if x == y)
        postotak_podudaranja = (podudaranja / duljina) * 100
        return postotak_podudaranja
    
    def split(self):
        return self.nukleotidi.split()

# Primjer upotrebe

gen1 = Geni("ATCG")
gen2 = Geni("AGAC")

mutacija = 'A'

novi_gen = gen1.spoji_gene(gen2)
gen1.dodaj_mutaciju(mutacija)
similarity = gen1.usporedi_gene(gen2)

#print(similarity)