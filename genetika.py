"""
Programski jezik za obradu podataka povezanih s genetikom. Jezik ima sljedeće funkcionalnosti:
- unos podataka iz konzole te automatsku dedukciju tipa unesenih podataka
- ispis podataka u konzolu
- operatore +, -, /, * koji rade na standardni način na realnim brojevima
- logičke operatore koji rade na standardni način
- operatore inkrementa ++ i += koji se koriste u petljama
- petlje koje se izvršavaju za zadani broj puta, koristeći različite mogućnosti inkrementa
- liste, koje mogu biti jednodimenzionalne ili dvodimenzionalne
- operatore na listama: remove koja uklanja dani element, removeIndeks koja uklanja element na danom indeksu,
  sort, clear, isEmpty, size, reverse
- funkcije koje mogu vratiti, ali i ne moraju nešto
- funkcije imaju lokalnu memoriju i lokalni doseg varijabli, ne postoje globalne varijable,
  nego ih je potrebno poslati funkciji kao argumente
- dopušteno je i moguće unutar jedne funkcije pozvati drugu
- mogućnost ispisa i upisa u tekstualnu datoteku
- jednolinijske komentare
- grananje u ovisnosti o istini danog uvjeta ili logičkog izraza
- tip podataka Variant, u kojeg se ucitava .csv datoteka
- funkcije consequencePercentage i diseasePercentage na tipu Variant, koje računaju redom postotak ucinka i postotak bolest u
  danim podacima
- tip Gen, koji u konstruktoru prima string aminokiselina
- operatori na tipu Gen:
    - operator +, koji kreira novi gen čije nukleotide su jednake spoju nukleotida danih gena, te alternativni
      način pisanja
    - operator ~, koji mutira dani gen, te alternativni način pisanja
    - operator %, koja izračunava postotak podudaranja dva gena, te alternativni način pisanja
- interaktivni način unosa podataka liniju po liniju, u programu interaktivniNacin.py

Sintaksa jezika:
- nije potrebno pisati jezik unutar klasa ili main funkcije
- nije potrebno zadavati tipove podataka
- komentari su jednolinijski, počinju s "---"
- svaka linija mora završiti s točkazarez ";", jedino petlje i grananje nemaju ";" nakon "}"
- u varijablu učitavamo koristeći input(ime_varijable), upisujemo u nju koristeći output(ime_varijable)
- aritmetički operatori su višemjesni
- grananje se deklarira i izvršava kao if(uvjet){}
- petlja deklarira i izvršava kao for(var=pocetak; var<broj; inkrement){}
- datoteku otvaramo koristeći ime_varijable_datoteke=open(ime_datoteke, mode), u nju pišemo kao WRITEOPTION(podatak),
  čitamo koristeći varijabla = READOPTION(ime_varijable_datoteke), te zatvaramo s close(ime_varijable_datoteke)
- READOPTION ima mogućnost čitanja cijele datoteke s READOPTION(ime_varijable_datoteke), n znakova sa
  READOPTION(ime_varijable_datoteke, n), ili linije s READOPTION(ime_varijable_datoteke, line)
- funkcije se deklariraju s ime_funckije=function(args){};, return nije potreban osim ako želimo povratni tip
- funkcije se pozivaju s call.ime_funkcije(args);
- listu stvaramo koristeći ime_liste=collection(), dodajemo koristeći append.ime_liste(args), te brišemo koristeći
  removeIndeks.ime_liste(indeks) ili remove.ime_liste(element), čistimo je sa clear.ime_liste(), na isti način
  pozivamo i reverse i sort, dok veličinu i je li lista prazna moramo spremiti u neku varijablu
- dvodimenzionalnu listu stvaramo tako da u početnu listu koristeći append dodamo novu kolekciju ili izmijenimo
  sadržaj na postojećem indeksu
- pristup elementu liste ostvarajemo s ime_liste[ind], ako je dvodimenzionalna lista koristimo ime_liste[ind1][ind2]
- tip Variant stvaramo s ime_var=variant(csv_datoteka), dok funkcije na njemu pozivamo na način
  ime_varijable = consequencePercentage.ime_var(ime_ucinka) i ime_varijable = diseasePercentage.ime_var(ime_bolesti)
- tip podataka Gen stvaramo s ime_varijable=gen(aminokiseline)
- kada ispisujemo tip Gen koristeći output onda zapravo ispisujemo njegove nukleotide
- operatori na tipu Gen, već objašnjeni, imaju sljedeće načine pisanja:
    - operator +, npr novi_gen=gen1+gen2+...+genN, ili alternativno novi_gen=[gen1, gen2]
    - operator ~, se može pisati kao ~var_gen, te će ga to mutirati, ali i na način var_gen=mutation(var_gen)
      šta će mutirati njega, ili kao novi_gen=mutation(var_gen), koje će mutirani gen spremiti u drugi gen,
      ali neće izmjeniti stari gen
    - operator %, koja vraća postotak podudarnosti između dva gena, piše se kao var_postotak=gen1%gen2
      ili alternativno var_postotak=similarity(gen1, gen2)
"""



from vepar import *
from varijante import *
from gen import *

class T(TipoviTokena):
    PLUS, MINUS, PUTA, KROZ = '+-*/'
    PLUSP, PLUSJ = '++', '+='
    JEDNAKO, MANJE, VECE = '=<>'
    MANJEJ, VECEJ, JEDNAKOJ, RAZLICITO = '<=', '>=', '==', '!='
    NEG, KONJ, DISJ, MUTACIJA, MOD = '!&|~%'
    UCINAK, BOLEST = 'consequencePercentage', 'diseasePercentage'
    OOTV, OZATV, VOTV, VZATV, ZAREZ, TOCKAZ, UOTV, UZATV, TOCKA = '(){},;[].'
    SIZE = 'size'
    VARIJANTA, GEN = 'variant', 'gen'
    IF, FOR, POZIV, REMOVE, REMOVEINDEX, CLEAR, ISEMPTY = 'if', 'for', 'call', 'remove', 'removeIndex', 'clear', 'isEmpty'
    FUNCTION, OPEN, CLOSE, READ, WRITE, LINE = 'function', 'open', 'close', 'READOPTION', 'WRITEOPTION', 'line'
    OUTPUT, RETURN, INPUT, NEWLINE, COLLECTION, APPEND = 'output', 'return', 'input', 'NEWLINE', 'collection', 'append'
    MUTACIJADVA, SLICNOST, SPLIT, SORT, REVERSE = 'mutation', 'similarity', 'split', 'sort', 'reverse'

    class NULL(Token):
        literal = 'null'
        def vrijednost(self, mem): return ""

    class BREAK(Token):
        literal = 'break'
        def izvrši(self, mem): raise Prekid

    class IME(Token):
        def vrijednost(self, mem): return mem[self]

    class BROJ(Token):
        def vrijednost(self, mem): return int(self.sadržaj)
        def optim(t): return t

    class STRING(Token):
        def vrijednost(self, mem): return self.sadržaj[1:-1]

@lexer
def gen(lex):
    for znak in lex:
        if znak.isspace(): lex.zanemari()
        elif znak == '=':
            yield lex.token(T.JEDNAKOJ if lex >= '=' else T.JEDNAKO)
        elif znak == '<':
            yield lex.token(T.MANJEJ if lex >= '=' else T.MANJE)
        elif znak == '>':
            yield lex.token(T.VECEJ if lex >= '=' else T.VECE)
        elif znak == '!':
            yield lex.token(T.RAZLICITO if lex >= '=' else T.NEG)
        elif znak == '+':
            if lex >= '+':
                yield lex.token(T.PLUSP)
            elif lex >= '=':
                yield lex.token(T.PLUSJ)
            else:
                yield lex.token(T.PLUS)
        elif znak == '-':
            if lex >= '-':
                lex >> '-'
                lex - '\n'
                lex.zanemari()
            else: yield lex.token(T.MINUS)
        elif znak.isdecimal():
            lex.prirodni_broj(znak)
            yield lex.token(T.BROJ)
        elif znak.islower() or znak.isupper():
            lex * str.isalnum
            yield lex.literal_ili(T.IME)
        elif znak == '"':
            lex - '"'
            yield lex.token(T.STRING)
        else:
            yield lex.literal(T)

##Beskontekstna gramatika
# start->naredbe naredba
# naredbe -> '' | naredbe naredba
# naredba -> petlja | grananje | ispis TOCKAZ | unos TOCKAZ | BREAK TOCKAZ | return TOCKAZ 
#                   | poziv_funkcije TOCKAZ | pridruzivanje TOCKAZ | zatvori TOCKAZ
#                   | append TOCKAZ | pisanje TOCKAZ | MUTACIJA OOTV IME OZATV
#                   | REMOVE TOCKA IME UOTV IME UZATV OOTV IME OZATV TOCKAZ | REMOVE TOCKA IME UOTV BROJ UZATV OOTV IME OZATV TOCKAZ | REMOVE TOCKA IME UOTV BROJ UZATV OOTV BROJ OZATV TOCKAZ |  REMOVE TOCKA IME UOTV IME UZATV OOTV BROJ OZATV TOCKAZ
#                   | REMOVEINDEX TOCKA IME UOTV IME UZATV OOTV IME OZATV TOCKAZ | REMOVEINDEX TOCKA IME UOTV BROJ UZATV OOTV IME OZATV TOCKAZ | REMOVEINDEX TOCKA IME UOTV BROJ UZATV OOTV BROJ OZATV TOCKAZ | REMOVEINDEX TOCKA IME UOTV IME UZATV OOTV BROJ OZATV TOCKAZ
#                   | SORT TOCKA IME OOTV OZATV TOCKAZ | SORT TOCKA IME UOTV IME UZATV OOTV OZATV TOCKAZ | SORT TOCKA IME UOTV BROJ UZATV OOTV OZATV TOCKAZ
#                   | REVERSE TOCKA IME OOTV OZATV TOCKAZ | REVERSE TOCKA IME UOTV IME UZATV OOTV OZATV TOCKAZ | REVERSE TOCKA IME UOTV BROJ UZATV OOTV OZATV TOCKAZ
# petlja -> for naredba | for VOTV naredbe VZATV
# for -> FOR OOTV IME_BROJA JEDNAKO BROJ TOCKAZ IME_BROJA MANJE BROJ TOCKAZ IME_BROJA inkrement OZATV
# inkrement -> PLUSP | PLUSJ BROJ
# grananje -> if naredba | if VOTV naredbe VZATV
# if -> IF OOTV izraz OZATV | IF OOTV bool OZATV
# ispis -> OUTPUT OOTV izraz OZATV | OUTPUT OOTV izraz NEWLINE OZATV | OUTPUT OOTV konst OZATV | OUTPUT OOTV konst NEWLINE OZATV
# unos -> INPUT OOTV IME OZATV
# return -> RETURN konst | RETURN IME
# konst -> STRING | BROJ
# poziv_funkcije -> POZIV TOCKA IME OOTV parametri OZATV
# parametri -> parametar ZAREZ parametar | parametar | ''
# parametar -> parametar ZAREZ parametar | konst | IME
# pridruzivanje -> IME JEDNAKO konst | IME JEDNAKO IME | IME JEDNAKO izraz | IME JEDNAKO bool 
#                   | IME JEDNAKO FUNCTION OOTV parametri OZATV VOTV naredbe VZATV | IME JEDNAKO OPEN OOTV STRING OZATV
#                   | IME JEDNAKO OPEN OOTV IME ZAREZ nacin OZATV | IME JEDNAKO citanje | IME JEDNAKO COLLECTION OOTV OZATV
#                   | IME JEDNAKO VARIJANTA OOTV STRING OZATV | IME JEDNAKO VARIJANTA OOTV IME OZATV
#                   | IME JEDNAKO GEN OOTV STRING OZATV | IME JEDNAKO GEN OOTV IME OZATV
#                   | IME JEDNAKO genizr | IME JEDNAKO IME MOD IME | IME JEDNAKO SIZE TOCKA IME OOTV OZATV
#                   | IME JEDNAKO SIZE TOCKA IME UOTV IME UZATV OOTV OZATV | IME JEDNAKO SIZE TOCKA IME UOTV BROJ UZATV OOTV OZATV
#                   | IME JEDNAKO poziv_funkcije | IME JEDNAKO MUTACIJADVA OOTV IME OZATV
#                   | IME JEDNAKO SPLIT OOTV IME OZATV | IME JEDNAKO SPLIT OOTV STRING OZATV
# genizr -> genizr PLUS GEN
# izraz -> clan | izraz PLUS clan | izraz MINUS clan
# clan -> BROJ| IME | GEN | clan PUTA BROJ | clan KROZ BROJ | UCINAK TOCKA IME OOTV IME OZATV | BOLEST TOCKA IME OOTV IME OZATV
#             | UCINAK TOCKA IME OOTV STRING OZATV | BOLEST TOCKA IME OOTV STRING OZATV | SLICNOST OOTV IME ZAREZ IME OZATV | OOTV izraz OZATV
# append -> APPEND TOCKA konst OOTV izraz (ZAREZ izraz | ZAREZ collection OOTV OZATV)* OZATV 
#         | APPEND TOCKA konst UOTV konst UZATV OOTV izraz (ZAREZ izraz | ZAREZ collection OOTV OZATV)* OZATV
# zatvori -> CLOSE OOTV IME OZATV
# citanje -> READLINE OOTV IME OZATV | READLINE OOTV IME ZAREZ LINE OZATV
# pisanje -> WRITELINE OOTV IME ZAREZ IME OZATV | WRITELINE OOTV IME ZAREZ konst OZATV
# bool -> NEG bool | IME MANJE IME | IME VECE IME | IME MANJEJ IME| IME VECEJ IME| bool KONJ IME | bool DISJ IME | IME JEDNAKOJ IME | IME RAZLICITO IME 
# element -> BROJ | STRING | UOTV elementi UZATV | UOTV UZATV
# elementi -> element | elementi ZAREZ element 

class P(Parser):
    def start(p) -> 'Program':
        rt.funkcije = Memorija(redefinicija=False)
        rt.mem = Memorija()
        naredbe = [p.naredba()]
        while not p > KRAJ: naredbe.append(p.naredba())
        return Program(naredbe)

    def naredba(p) -> 'petlja|pridruzivanje|grananje|poziv|ispis|unos|remove|mutacija|append|Return|BREAK':
        if p > T.FOR: return p.petlja()
        elif p >= T.RETURN:
            za_return = Return(p.izraz())
            p >> T.TOCKAZ
            return za_return
        #obzirom da mutacija može djelovati sama na sebe, mozemo je pozvati i bez spremanja u drugu varijablu
        elif p > T.MUTACIJA: 
            mutacija = p.mutacija()
            p >> T.TOCKAZ
            return mutacija
        elif p > T.MUTACIJADVA:
            p >> T.MUTACIJADVA
            p >> T.OOTV
            var = p >> T.IME
            p >> T.OZATV
            p >> T.TOCKAZ
            return Mutacija(var)
        elif p > T.IME:
            pridruzivanje = p.pridruzivanje()
            p >> T.TOCKAZ
            return pridruzivanje
        elif p > T.APPEND:
            append = p.append()
            p >> T.TOCKAZ
            return append
        elif p > T.REMOVE:
            remove = p.remove()
            p >> T.TOCKAZ
            return remove
        elif p > T.REMOVEINDEX:
            removeIndex = p.removeIndex()
            p >> T.TOCKAZ
            return removeIndex
        elif p > T.CLEAR:
            clear = p.clear()
            p >> T.TOCKAZ
            return clear
        elif p > T.SORT:
            sort = p.sort()
            p >> T.TOCKAZ
            return sort
        elif p > T.REVERSE:
            reverse = p.reverse()
            p >> T.TOCKAZ
            return reverse
        elif p > T.IF: return p.grananje()
        elif p > T.CLOSE:
            zatvori = p.zatvori()
            p >> T.TOCKAZ
            return zatvori
        elif p > T.WRITE:
            pisi = p.pisi()
            p >> T.TOCKAZ
            return pisi
        elif p > T.POZIV:
            poziv = p.poziv()
            p >> T.TOCKAZ
            return poziv
        elif p > T.OUTPUT:
            ispis = p.ispis()
            p >> T.TOCKAZ
            return ispis
        elif p > T.INPUT:
            unos = p.unos()
            p >> T.TOCKAZ
            return unos
        elif br := p >> T.BREAK:
            p >> T.TOCKAZ
            return br

    def mutacija(p)-> 'Mutacija':
        p >> T.MUTACIJA
        ime = p >> T.IME
        return Mutacija(ime)

    #vraca AST koji cisti listu, ili cisti listu na indeksu druge liste u slucaju 2d liste
    def clear(p) -> 'Clear|Clear2d':
        p >> T.CLEAR
        p >> T.TOCKA
        ime = p >> T.IME
        if p > T.UOTV:
            p >> T.UOTV
            ind = p >> {T.IME, T.BROJ}
            p >> T.UZATV
            p >> T.OOTV
            p >> T.OZATV
            return Clear2d(ime, ind)
        else:
            p >> T.OOTV
            p >> T.OZATV
            return Clear(ime)
        
    def sort(p) -> 'Sort|Sort2d':
        p >> T.SORT
        p >> T.TOCKA
        ime = p >> T.IME
        if p > T.UOTV:
            p >> T.UOTV
            ind = p >> {T.IME, T.BROJ}
            p >> T.UZATV
            p >> T.OOTV
            p >> T.OZATV
            return Sort2d(ime, ind)
        else:
            p >> T.OOTV
            p >> T.OZATV
            return Sort(ime)
        
    def reverse(p) -> 'Reverse|Reverse2d':
        p >> T.REVERSE
        p >> T.TOCKA
        ime = p >> T.IME
        if p > T.UOTV:
            p >> T.UOTV
            ind = p >> {T.IME, T.BROJ}
            p >> T.UZATV
            p >> T.OOTV
            p >> T.OZATV
            return Reverse2d(ime, ind)
        else:
            p >> T.OOTV
            p >> T.OZATV
            return Reverse(ime)
   
    #vraca AST koji brise element liste na danom indexu
    def removeIndex(p) -> 'RemoveIndex|RemoveIndex2d':
        p >> T.REMOVEINDEX
        p >> T.TOCKA
        ime = p >> T.IME
        if p > T.UOTV:
            p >> T.UOTV
            ind = p >> {T.IME, T.BROJ}
            p >> T.UZATV
            p >> T.OOTV
            argument = p >> {T.IME, T.BROJ}
            p >> T.OZATV
            return RemoveIndex2d(ime, argument, ind)
        else:
            p >> T.OOTV
            argument = p >> {T.IME, T.BROJ}
            p >> T.OZATV
            return RemoveIndex(ime, argument)

    #vraca AST koji brise dani element liste
    def remove(p) -> 'Remove|Remove2d':
        p >> T.REMOVE
        p >> T.TOCKA
        ime = p >> T.IME
        if p > T.UOTV:
            p >> T.UOTV
            ind = p >> {T.IME, T.BROJ}
            p >> T.UZATV
            p >> T.OOTV
            argument = p >> {T.IME, T.BROJ}
            p >> T.OZATV
            return Remove2d(ime, argument, ind)
        else:
            p >> T.OOTV
            argument = p >> {T.IME, T.BROJ}
            p >> T.OZATV
            return Remove(ime, argument)

    #vraca AST za upis u datoteku
    def pisi(p) -> 'Pisi':
        p >> T.WRITE
        p >> T.OOTV
        ime = p >> T.IME
        p >> T.ZAREZ
        argument = p >> {T.IME, T.BROJ, T.STRING}
        p >> T.OZATV
        return Pisi(ime, argument)
    
    #vraca AST za zatvaranje datoteke
    def zatvori(p) -> 'Zatvaranje':
        p >> T.CLOSE
        p >> T.OOTV
        ime = p >> T.IME
        p >> T.OZATV
        return Zatvaranje(ime)

    #vraca AST koji poziva funkciju koja ne sprema nigdje svoju vrijednost
    def poziv(p) -> 'Poziv':
        p >> T.POZIV
        p >> T.TOCKA
        ime = p >> T.IME
        p >> T.OOTV
        argumenti = []
        if p >  {T.IME, T.BROJ}:
            argumenti.append(p.izraz())
            while p >= T.ZAREZ : argumenti.append(p.izraz())
        p >> T.OZATV
        return Poziv(ime, argumenti)
    
    #vraca AST koji dodaje na kraj liste dane elemente
    def append(p) -> 'Append|Append2d':
        p >> T.APPEND
        p >> T.TOCKA
        ime = p >> T.IME
        if p > T.UOTV:
            p >> T.UOTV
            ind = p >> {T.IME, T.BROJ}
            p >> T.UZATV
            p >> T.OOTV
            argumenti = []
            if p >  {T.IME, T.BROJ, T.COLLECTION, T.OOTV}:
                if p > T.COLLECTION:
                    p >> T.COLLECTION
                    p >> T.OOTV
                    p >> T.OZATV
                    argumenti.append("collection()")
                else:
                    argumenti.append(p.izraz())
                while p >= T.ZAREZ : 
                    if p > T.COLLECTION:
                        p >> T.COLLECTION
                        p >> T.OOTV
                        p >> T.OZATV
                        argumenti.append("collection()")
                    else:
                        argumenti.append(p.izraz())
            p >> T.OZATV
            return Append2d(ime, argumenti, ind)
        else:
            p >> T.OOTV
            argumenti = []
            if p >  {T.IME, T.BROJ, T.COLLECTION, T.OOTV}:
                if p > T.COLLECTION:
                    p >> T.COLLECTION
                    p >> T.OOTV
                    p >> T.OZATV
                    argumenti.append("collection()")
                else:
                    argumenti.append(p.izraz())
                while p >= T.ZAREZ : 
                    if p > T.COLLECTION:
                        p >> T.COLLECTION
                        p >> T.OOTV
                        p >> T.OZATV
                        argumenti.append("collection()")
                    else:
                        argumenti.append(p.izraz())
            p >> T.OZATV
            return Append(ime, argumenti)

    def grananje(p) -> 'Grananje':
        p >> T.IF, p >> T.OOTV
        value = p.bool()
        p >> T.OZATV
        if p >= T.VOTV:
            blok = []
            while not p >= T.VZATV: blok.append(p.naredba())
        else: blok = [p.naredba()]
        return Grananje(value, blok)
    
    def bool(p) -> 'Bool':
        lijevo = p.izraz()
        op = p >= {T.JEDNAKOJ, T.MANJE, T.VECE, T.MANJEJ, T.VECEJ, T.RAZLICITO,T.KONJ, T.NEG, T.DISJ}
        desno = p.izraz()
        return Bool(lijevo, op, desno)

    def ispis(p) -> 'Ispis':
        novi_red = False
        p >> T.OUTPUT
        p >> T.OOTV
        if p > {T.BROJ, T.IME, T.OOTV}:
            trenutno = p.izraz()
        elif p > T.STRING:
            trenutno = p >> T.STRING
        if p > T.NEWLINE:
            p >> T.NEWLINE
            novi_red = True
        p >> T.OZATV
        return Ispis(trenutno, novi_red)
    
    def pridruzivanje(p) -> 'Pridruzivanje|Funkcija|Varijanta|Otvaranje|Citanje|Kolekcija|Pridruzivanje2d|PridruzivanjeIndeks|KolekcijaIndeks':
        lijevo = p >> T.IME
        if p > T.UOTV:
            ind2d = "nista"
            p >> T.UOTV
            ind = p >> {T.IME, T.BROJ}
            p >> T.UZATV
            if p > T.UOTV:
                p >> T.UOTV
                ind2d = p >> {T.IME, T.BROJ}
                p >> T.UZATV
            p >> T.JEDNAKO
            if p > {T.IME, T.BROJ}:
                desno = p.izraz()
                if ind2d != "nista":
                    return Pridruzivanje2d(lijevo, desno, ind, ind2d)
                else:
                    return PridruzivanjeIndeks(lijevo, desno, ind)
            elif p > T.STRING:
                desno = p >> T.STRING
                return PridruzivanjeIndeks(lijevo, desno, ind)
            elif p > T.COLLECTION:
                p >> T.COLLECTION
                p >> T.OOTV
                p >> T.OZATV
                return KolekcijaIndeks(lijevo, ind)
        p >> T.JEDNAKO
        if p > {T.IME, T.BROJ, T.MINUS, T.BOLEST, T.UCINAK, T.SLICNOST, T.OOTV}:
            desno = p.izraz()
            return Pridruzivanje(lijevo, desno)
        elif p > T.SPLIT:
            p >> T.SPLIT
            p >> T.OOTV
            ime = p >> {T.IME, T.STRING}
            p >> T.OZATV
            return Pridruzivanje(lijevo, Split(ime))
        elif p > T.STRING:
            desno = p >> T.STRING
            return Pridruzivanje(lijevo, desno)
        elif p > T.UOTV:
            p >> T.UOTV
            desno = p.genIzr()
            p >> T.UZATV
            return Pridruzivanje(lijevo, desno)
        elif p > T.VARIJANTA:
            p >> T.VARIJANTA
            p >> T.OOTV
            desno =  p >> {T.IME, T.STRING}
            p >> T.OZATV
            return Pridruzivanje(lijevo, Varijanta(desno))
        elif p > T.GEN:
            p >> T.GEN
            p >> T.OOTV
            desno = p >> {T.IME, T.STRING}
            p >> T.OZATV
            return Pridruzivanje(lijevo, Gen(desno))
        elif p > T.MUTACIJADVA:
            p >> T.MUTACIJADVA
            p >> T.OOTV
            desno = p >> T.IME
            p >> T.OZATV
            return Pridruzivanje(lijevo, MutacijaDva(desno))       
        elif p > T.READ:
            p >> T.READ
            p >> T.OOTV
            koliko = 0
            desno = p >> T.IME
            if p > T.ZAREZ:
                p >> T.ZAREZ
                if p > T.LINE:
                    p >> T.LINE
                    koliko = "line"
                else:
                    broj = p.izraz().vrijednost(rt.mem)
                    koliko = broj
            p >> T.OZATV
            return Citanje(lijevo, desno, koliko)
        elif p > T.COLLECTION:
            p >> T.COLLECTION
            p >> T.OOTV
            p >> T.OZATV
            return Kolekcija(lijevo)
        elif p > T.OPEN:
            p >> T.OPEN
            p >> T.OOTV
            ime = p >> {T.STRING, T.IME}
            p >> T.ZAREZ
            nacin = p >> T.STRING
            if nacin.vrijednost(rt.mem)!="r" and nacin.vrijednost(rt.mem)!="a" and nacin.vrijednost(rt.mem)!="w":
                assert False, 'Nacin mora biti "r", "a" ili "w"' 
            p >> T.OZATV
            return Otvaranje(lijevo, ime , nacin)
        elif p > T.POZIV:
            p >> T.POZIV
            p >> T.TOCKA
            ime = p>>T.IME
            p >> T.OOTV
            argumenti = []
            if p >  {T.IME, T.BROJ}:
                argumenti.append(p.izraz())
                while p >= T.ZAREZ : argumenti.append(p.izraz())
            p >> T.OZATV
            return Pridruzivanje(lijevo, Poziv(ime, argumenti))
        elif p > T.ISEMPTY:
            p >> T.ISEMPTY
            p >> T.TOCKA
            ime = p >> T.IME
            ind = "nista"
            if p > T.UOTV:
                p >> T.UOTV
                ind = p >> {T.IME, T.BROJ}
                p >> T.UZATV
                p >> T.OOTV
                p >> T.OZATV
                return Pridruzivanje(lijevo, IsEmpty(ime, ind))
            else:
                p >> T.OOTV
                p >> T.OZATV
                return Pridruzivanje(lijevo, IsEmpty(ime, ind))
        elif p > T.SIZE:
            p >> T.SIZE
            p >> T.TOCKA
            ime = p >> T.IME
            if p > T.UOTV:
                p >> T.UOTV
                ind = p >> {T.IME, T.BROJ}
                p >> T.UZATV
                p >> T.OOTV
                p >> T.OZATV
                return Pridruzivanje(lijevo, Size2d(ime, ind))
            else:
                p >> T.OOTV
                p >> T.OZATV
                return Pridruzivanje(lijevo, Size(ime))
        elif p > T.FUNCTION:
            p >> T.FUNCTION
            p >> T.OOTV
            argumenti = []
            if p > T.IME:
                argumenti.append(p >> T.IME)
                while p >= T.ZAREZ : argumenti.append(p >> T.IME)
            p >> T.OZATV
            if p >= T.VOTV:
                blok = []
                while not p >= T.VZATV: blok.append(p.naredba())
            else: blok = [p.naredba()]
            return Funkcija(lijevo, argumenti, blok)
        else:
            assert False, 'nepokriveni slucaj'
    
    def unos(p) -> 'Unos':
        p >> T.INPUT
        p >> T.OOTV
        varijabla = p >> T.IME
        p >> T.OZATV
        return Unos(varijabla)

    def petlja(p) -> 'Petlja':
        kriva_varijabla = SemantičkaGreška(
            'Sva tri dijela for-petlje moraju imati istu varijablu.')
        p >> T.FOR, p >> T.OOTV
        i = p >> T.IME
        p >> T.JEDNAKO
        početak = p >> {T.BROJ, T.IME}
        if p > T.UOTV:
            p >> T.UOTV
            ind = p >> {T.IME, T.BROJ}
            p >> T.UZATV
            ind2d = "nista"
            if p > T.UOTV:
                p >> T.UOTV
                ind2d = p >> {T.IME, T.BROJ}
                p >> T.UZATV
            početak = Dohvati(početak, ind, ind2d)
        p >> T.TOCKAZ

        if (p >> T.IME) != i: raise kriva_varijabla
        p >> T.MANJE
        granica = p >> {T.BROJ, T.IME}
        if p > T.UOTV:
            p >> T.UOTV
            ind = p >> {T.IME, T.BROJ}
            p >> T.UZATV
            ind2d = "nista"
            if p > T.UOTV:
                p >> T.UOTV
                ind2d = p >> {T.IME, T.BROJ}
                p >> T.UZATV
            granica = Dohvati(granica, ind, ind2d)
        p >> T.TOCKAZ

        if (p >> T.IME) != i: raise kriva_varijabla
        if p >= T.PLUSP: inkrement = nenavedeno
        elif p >> T.PLUSJ: 
            inkrement = p >> {T.BROJ, T.IME}
            if p > T.UOTV:
                p >> T.UOTV
                ind = p >> {T.IME, T.BROJ}
                p >> T.UZATV
                ind2d = "nista"
                if p > T.UOTV:
                    p >> T.UOTV
                    ind2d = p >> {T.IME, T.BROJ}
                    p >> T.UZATV
                inkrement = Dohvati(inkrement, ind, ind2d)
        p >> T.OZATV

        if p >= T.VOTV:
            blok = []
            while not p >= T.VZATV: blok.append(p.naredba())
        else: blok = [p.naredba()]
        return Petlja(i, početak, granica, inkrement, blok)

    def izraz(p) -> 'Zbroj|član':
        trenutni = [p.član()]
        while ...:
            if p >= T.PLUS: trenutni.append(p.član())
            elif p >= T.MINUS: trenutni.append(Suprotan(p.član()))
            else: return Zbroj.ili_samo(trenutni)


    def član(p) -> 'Umnožak|broj':
        trenutni = [p.broj()]
        if isinstance(trenutni[0], Postotak):
            return trenutni[0]
        while ...:
            if p >= T.PUTA: trenutni.append(p.broj())
            elif p >= T.KROZ: trenutni.append(Reciprocan(p.broj()))
            else: return Umnožak.ili_samo(trenutni)
    
    def broj(p) -> 'Broj|Dohvati|Ucinak|Bolest|Postotak|NegativniBroj':
        if p > T.BOLEST:
            p >> T.BOLEST
            p >> T.TOCKA
            var = p >> T.IME
            p >> T.OOTV
            ime = p >> {T.IME, T.STRING}
            p >> T.OZATV
            return Bolest(var, ime)
        elif p > T.OOTV:
            p >> T.OOTV
            iz = p.izraz()
            p >> T.OZATV
            return iz 
        elif p > T.SLICNOST:
            p >> T.SLICNOST
            p >> T.OOTV
            prvi = p >> T.IME
            p >> T.ZAREZ
            drugi = p >> T.IME
            p >> T.OZATV
            return Postotak(prvi, drugi)
        elif p > T.UCINAK:
            p >> T.UCINAK
            p >> T.TOCKA
            var = p >> T.IME
            p >> T.OOTV
            ime = p >> {T.IME, T.STRING}
            p >> T.OZATV
            return Ucinak(var, ime)
        elif p > T.MUTACIJADVA:
            p >> T.MUTACIJADVA
            p >> T.OOTV
            var = p >> T.IME
            p >> T.OZATV
            return MutacijaDva(var)
        elif p > T.MINUS:
            p >> T.MINUS
            broj = p >> {T.BROJ, T.IME}
            return NegativniBroj(broj)
        elif broj := p >> {T.BROJ, T.IME}:
            if p > T.MOD:
                p >> T.MOD
                desno = p >> T.IME
                return Postotak(broj, desno)
            if p > T.UOTV:
                p >> T.UOTV
                ind = p >> {T.IME, T.BROJ}
                p >> T.UZATV
                ind2d = "nista"
                if p > T.UOTV:
                    p >> T.UOTV
                    ind2d = p >> {T.IME, T.BROJ}
                    p >> T.UZATV
                return Dohvati(broj, ind, ind2d)
            return Broj(broj)
    
    def genIzr(p):
        trenutni = [p >> T.IME]
        while ...:
            if p >= T.ZAREZ: 
                trenutni.append(p >> T.IME)
            else: return ZbrojGena.ili_samo(trenutni)
    

nula, jedan = Token(T.BROJ, '0'), Token(T.BROJ, '1')

class Split(AST):
    naziv: 'ime'
    
    def vrijednost(self, mem):
        return self.naziv.vrijednost(mem).split()

#AST-ovi koji koriste klase Geni i Varijanta su implementirani koristeći članske funkcije tih klase
#te preopterećene operatore na njima
class Mutacija(AST):
    naziv: 'ime'
    
    def izvrši(self, mem):
        ~self.naziv.vrijednost(mem)

class MutacijaDva(AST):
    naziv: 'ime'
    
    def vrijednost(self, mem):
        return self.naziv.vrijednost(mem).dodaj_mutaciju_dva()

class Postotak(AST):
    prvi: 'broj'
    drugi: 'desno'

    def vrijednost(self, mem):
        return self.prvi.vrijednost(mem)%self.drugi.vrijednost(mem)

class ZbrojGena(AST):
    geni: 'izraz*'

    def vrijednost(self, mem):
        novi = Geni("")
        for g in self.geni:
            novi = novi + g.vrijednost(mem)
        return novi


class Bolest(AST):
    varijanta: 'var'
    naziv: 'ime'

    def vrijednost(self, mem):
        var = self.varijanta.vrijednost(mem)
        return var.izracunaj_postotak_bolesti(self.naziv.vrijednost(mem))
    
class Ucinak(AST):
    varijanta: 'var'
    naziv: 'ime'

    def vrijednost(self, mem):
        var = self.varijanta.vrijednost(mem)
        return var.postotak_predvidenog_ucinka(self.naziv.vrijednost(mem))

class Varijanta(AST):
    ime: 'desno'
    
    def vrijednost(self, mem):
        return Varijante(self.ime.vrijednost(mem))
    
class Gen(AST):
    ime: 'desno'
    
    def vrijednost(self, mem):
        return Geni(self.ime.vrijednost(mem))

class IsEmpty(AST):
    naziv: 'ime'
    indeks: 'ind'

    def vrijednost(self, mem):
        lista = mem[self.naziv]
        if self.indeks == "nista":
            return not lista
        else:
            lista = mem[self.naziv]
            lista2d = lista[self.indeks.vrijednost(mem)]
            return not lista2d

class Remove(AST):
    naziv: 'ime'
    arg: 'argument'

    def izvrši(self, mem):
        lista = mem[self.naziv]
        lista.remove(self.arg.vrijednost(mem))
        mem[self.naziv] = lista

class Remove2d(AST):
    naziv: 'ime'
    arg: 'argument'
    indeks: 'ind'

    def izvrši(self, mem):
        lista = mem[self.naziv]
        lista2d = lista[self.indeks.vrijednost(mem)]
        lista2d.remove(self.arg.vrijednost(mem))
        lista[self.indeks.vrijednost(mem)] = lista2d
        mem[self.naziv] = lista

class RemoveIndex(AST):
    naziv: 'ime'
    arg: 'argument'

    def izvrši(self, mem):
        lista = mem[self.naziv]
        lista.pop(self.arg.vrijednost(mem))
        mem[self.naziv] = lista

class RemoveIndex2d(AST):
    naziv: 'ime'
    arg: 'argument'
    indeks: 'ind'

    def izvrši(self, mem):
        lista = mem[self.naziv]
        lista2d = lista[self.indeks.vrijednost(mem)]
        lista2d.pop(self.arg.vrijednost(mem))
        lista[self.indeks.vrijednost(mem)] = lista2d
        mem[self.naziv] = lista

class Clear(AST):
    naziv: 'ime'

    def izvrši(self, mem):
        lista = mem[self.naziv]
        lista.clear()
        mem[self.naziv] = lista

class Clear2d(AST):
    naziv: 'ime'
    indeks: 'ind'

    def izvrši(self, mem):
        lista = mem[self.naziv]
        lista2d = lista[self.indeks.vrijednost(mem)]
        lista2d.clear()
        lista[self.indeks.vrijednost(mem)] = lista2d
        mem[self.naziv] = lista

class Sort(AST):
    naziv: 'ime'

    def izvrši(self, mem):
        lista = mem[self.naziv]
        lista.sort()
        mem[self.naziv] = lista

class Sort2d(AST):
    naziv: 'ime'
    indeks: 'ind'

    def izvrši(self, mem):
        lista = mem[self.naziv]
        lista2d = lista[self.indeks.vrijednost(mem)]
        lista2d.sort()
        lista[self.indeks.vrijednost(mem)] = lista2d
        mem[self.naziv] = lista

class Reverse(AST):
    naziv: 'ime'

    def izvrši(self, mem):
        lista = mem[self.naziv]
        lista.reverse()
        mem[self.naziv] = lista

class Reverse2d(AST):
    naziv: 'ime'
    indeks: 'ind'

    def izvrši(self, mem):
        lista = mem[self.naziv]
        lista2d = lista[self.indeks.vrijednost(mem)]
        lista2d.reverse()
        lista[self.indeks.vrijednost(mem)] = lista2d
        mem[self.naziv] = lista

class Size(AST):
    naziv: 'ime'

    def vrijednost(self, mem):
        lista = mem[self.naziv]
        return len(lista)

class Size2d(AST):
    naziv: 'ime'
    indeks: 'ind'

    def vrijednost(self, mem):
        lista = mem[self.naziv]
        lista2d = lista[self.indeks.vrijednost(mem)]
        return len(lista2d)

class Dohvati(AST):
    ime: 'broj'
    indeks: 'ind'
    indeks2d: 'ind2d'

    def vrijednost(self, mem):
        lista = mem[self.ime]
        if self.indeks2d == "nista":
            return lista[self.indeks.vrijednost(mem)]
        else:
            lista = mem[self.ime]
            lista2d = lista[self.indeks.vrijednost(mem)]
            return lista2d[self.indeks2d.vrijednost(mem)]
    
class PridruzivanjeIndeks(AST):
    prvi: 'lijevo'
    drugi: 'desno'
    indeks: 'ind'

    def izvrši(self, mem):
        lista = mem[self.prvi]
        lista[self.indeks.vrijednost(mem)] = self.drugi.vrijednost(mem)
        mem[self.prvi] = lista

class Pridruzivanje2d(AST):
    prvi: 'lijevo'
    drugi: 'desno'
    indeks: 'ind'
    indeks2d: 'ind2d'

    def izvrši(self, mem):
        lista = mem[self.prvi]
        lista2d = lista[self.indeks.vrijednost(mem)]
        lista2d[self.indeks2d.vrijednost(mem)] = self.drugi.vrijednost(mem)
        lista[self.indeks.vrijednost(mem)] = lista2d
        mem[self.prvi] = lista

class KolekcijaIndeks(AST):
    naziv: 'ime'
    indeks: 'ind'

    def izvrši(self, mem):
        lista = mem[self.naziv]
        lista[self.indeks.vrijednost(mem)] = []
        mem[self.naziv] = lista

class Broj(AST):
    trenutno: 'IME|BROJ'
    def vrijednost(broj, mem):
        return broj.trenutno.vrijednost(mem)
    
class NegativniBroj(AST):
    trenutno: 'IME|BROJ'
    def vrijednost(broj, mem):
        return -1*broj.trenutno.vrijednost(mem)

class Kolekcija(AST):
    naziv: 'ime'

    def izvrši(self, mem):
        mem[self.naziv] = []

class Pisi(AST):
    naziv: 'ime'
    sadrzaj: 'argument'

    def izvrši(self, mem):
        self.naziv.vrijednost(mem).write(str(self.sadrzaj.vrijednost(mem)))

class Citanje(AST):
    prvi: 'lijevo'
    drugi: 'desno'
    kolicina: 'koliko'

    def izvrši(self, mem):
        if self.kolicina == 0:
            mem[self.prvi] = self.drugi.vrijednost(mem).read()
        elif self.kolicina=="line":
            value = self.drugi.vrijednost(mem).readline()
            value = value.replace('\n', '')
            mem[self.prvi] = value
        else:
            mem[self.prvi] = self.drugi.vrijednost(mem).read(self.kolicina)

class Otvaranje(AST):
    naziv: 'lijevo'
    file: 'ime'
    mode: 'nacin'

    def izvrši(self, mem):
        mem[self.naziv] = open(self.file.vrijednost(mem), self.mode.vrijednost(mem))

class Zatvaranje(AST):
    naziv: 'ime'
    def izvrši(self, mem):
        mem[self.naziv] = self.naziv.vrijednost(mem).close()

class Funkcija(AST):
    ime: 'lijevo'
    parametri: 'argumenti*'
    tijelo: 'blok*'

    def izvrši(funkcija, mem):
        rt.funkcije[funkcija.ime]=funkcija

    def pozovi(funkcija,lokalna_memorija):
        try: 
            for naredba in funkcija.tijelo: naredba.izvrši(lokalna_memorija)
        except Povratak as exc: return exc.preneseno

class Poziv(AST):
    ime_funkcije: 'ime'
    parametri: 'argumenti*'

    def napravi_memoriju(self, mem):
        lokalna = Memorija()
        funkcija = rt.funkcije[self.ime_funkcije]
        if len(self.parametri)!= len(funkcija.parametri):
            raise SemantičkaGreška('Funkcija je primila pogrešan broj argumenata')
        for parametar, argument in zip(self.parametri, funkcija.parametri):
            lokalna[argument] = parametar.vrijednost(mem)
        return lokalna


    def izvrši(self, mem):
        funkcija = rt.funkcije[self.ime_funkcije]
        lokalna_memorija = self.napravi_memoriju(mem)
        funkcija.pozovi(lokalna_memorija)

    def vrijednost(self, mem):
        funkcija = rt.funkcije[self.ime_funkcije]
        lokalna_memorija = self.napravi_memoriju(mem)
        return funkcija.pozovi(lokalna_memorija)
    
class Append(AST):
    naziv: 'ime'
    argumenti: 'argumenti*'

    def izvrši(self, mem):
        lista = mem[self.naziv]
        for arg in self.argumenti:
            if arg == "collection()":
                lista.append([])
            else:
                lista.append(arg.vrijednost(mem))
        mem[self.naziv] = lista

class Append2d(AST):
    naziv: 'ime'
    argumenti: 'argumenti*'
    indeks: 'ind'

    def izvrši(self, mem):
        lista = mem[self.naziv]
        lista2d = lista[self.indeks.vrijednost(mem)]
        for arg in self.argumenti:
            if arg == "collection()":
                lista2d.append([])
            else:
                lista2d.append(arg.vrijednost(mem))
        lista[self.indeks.vrijednost(mem)] = lista2d
        mem[self.naziv] = lista


class Return(AST):
    što: 'argument'
    def izvrši(self, mem):
        raise Povratak(self.što.vrijednost(mem))

class Grananje(AST):
    istinitost: 'value'
    onda: 'naredba*'

    def izvrši(grananje, mem):
        if grananje.istinitost.vrijednost(mem):
            for naredba in grananje.onda: naredba.izvrši(mem)

class Pridruzivanje(AST):
    prvi: 'lijevo'
    drugi: 'desno'

    def izvrši(self, mem):
        mem[self.prvi] = self.drugi.vrijednost(mem)
        

class Bool(AST):
    prvi: 'lijevo'
    operator: 'op'
    drugi: 'desno'

    def vrijednost(bool, mem):
        if bool.operator ^ T.JEDNAKOJ:
            return bool.prvi.vrijednost(mem)==bool.drugi.vrijednost(mem)
        elif bool.operator ^ T.MANJE:
            return bool.prvi.vrijednost(mem)<bool.drugi.vrijednost(mem)
        elif bool.operator ^ T.MANJEJ:
            return bool.prvi.vrijednost(mem)<=bool.drugi.vrijednost(mem)
        elif bool.operator ^ T.VECE:
            return bool.prvi.vrijednost(mem)>bool.drugi.vrijednost(mem)
        elif bool.operator ^ T.VECEJ:
            return bool.prvi.vrijednost(mem)>=bool.drugi.vrijednost(mem)
        elif bool.operator ^ T.RAZLICITO:
            return bool.prvi.vrijednost(mem)!=bool.drugi.vrijednost(mem)
        elif bool.operator ^ T.KONJ:
            return bool.prvi.vrijednost(mem) and bool.drugi.vrijednost(mem)
        elif bool.operator ^ T.DISJ:
            return bool.prvi.vrijednost(mem) or bool.drugi.vrijednost(mem)
        elif bool.operator ^ T.NEG:
            return not bool.prvi.vrijednost(mem)
        else:
            assert False, 'nepokriveni slucaj'

class Petlja(AST):
    varijabla: 'IME'
    početak: 'BROJ'
    granica: 'BROJ'
    inkrement: 'BROJ?'
    blok: 'naredba*'

    def izvrši(petlja, mem):
        kv = petlja.varijabla  # kontrolna varijabla petlje
        mem[kv] = petlja.početak.vrijednost(mem)
        while mem[kv] < petlja.granica.vrijednost(mem):
            try:
                for naredba in petlja.blok: naredba.izvrši(mem)
            except Prekid: break
            inkr = petlja.inkrement
            mem[kv] += inkr.vrijednost(mem) if inkr else 1

class Zbroj(AST):
    pribrojnici: 'izraz*'

    def vrijednost(zbroj, mem):
        rez = 0
        for pr in zbroj.pribrojnici:
            if isinstance(pr.vrijednost(mem), str):
                rez = rez + int(pr.vrijednost(mem))
            else:    
                rez = rez + pr.vrijednost(mem)
        return rez
    
    def optim(zbroj):
        opt_pribr = [pribrojnik.optim() for pribrojnik in zbroj.pribrojnici]
        opt_pribr = [x for x in opt_pribr if x != nula]
        if not opt_pribr: return nula
        return Zbroj.ili_samo(opt_pribr)

class Umnožak(AST):
    faktori: 'izraz*'

    def vrijednost(umnožak, mem):
        return math.prod(faktor.vrijednost(mem) for faktor in umnožak.faktori)

    def optim(umnožak):
        opt_fakt = [faktor.optim() for faktor in umnožak.faktori]
        if nula in opt_fakt: return nula
        opt_fakt = [x for x in opt_fakt if x != jedan]
        if not opt_fakt: return jedan
        else: return Umnožak.ili_samo(opt_fakt)

class Suprotan(AST):
    od: 'izraz'
    def vrijednost(self, mem): return -self.od.vrijednost(mem)

class Reciprocan(AST):
    od: 'clan'
    def vrijednost(self, mem):
        if self.od.vrijednost(mem) != 0:
            return 1/self.od.vrijednost(mem)
        else:
            raise ArithmeticError('Ne dijeli s nulom')


class Prekid(NelokalnaKontrolaToka): """Signal koji šalje naredba break."""
class Povratak(NelokalnaKontrolaToka): """Signal koji šalje naredba vrati."""


class Ispis(AST):
    trenutno: 'IME|BROJ|STRING'
    novi_red: 'True|False'
    def izvrši(ispis, mem):
        t = ispis.trenutno.vrijednost(mem)
        print(t)
        if ispis.novi_red == True:
            print()

class Unos(AST):
    varijabla: 'IME'
    def izvrši(unos, mem):
        v = unos.varijabla
        if v ^ T.IME:
            prompt = f' Unesite varijablu {v.sadržaj}: '
            unos = input(prompt)
            if unos.isnumeric():
                if isinstance(unos, float):
                    mem[v] = float(unos)
                else:
                    mem[v] = int(unos)
            else:
                mem[v] = str(unos)
        else: assert False, f'Nepoznat tip varijable {v}'

class Program(AST):
    naredbe: 'naredba*'

    def izvrši(program):
        try:  # break izvan petlje je zapravo sintaksna greška - kompliciranije
            for naredba in program.naredbe: naredba.izvrši(rt.mem)
        except Prekid: raise SemantičkaGreška('nedozvoljen break izvan petlje')
