import random
import time
from miller_rabin import czy_pierwsza_mr

def losuj_pierwsza(rng, k):
    maska = 1 | 1 << k-1 | 1 << k-2
    
    kandydat = rng.getrandbits(k) | maska

    while(not czy_pierwsza_mr(kandydat)):
        kandydat = rng.getrandbits(k) | maska

    return kandydat

def stworz_pule(k, rozmiar):
    rng = random.SystemRandom()
    pula = []
    while len(pula) < rozmiar:
        x = losuj_pierwsza(rng, k)
        if x not in pula: pula.append(x)
    return pula


def generator(nazwa, k, ziarno=None, pula=None):   
    if nazwa == "G1":
        if ziarno is None:
            ziarno = random.randrange(65536) #16bitów
        rng = random.Random(ziarno)

    elif nazwa == "G2":
        if pula is None: raise ValueError("nie podano puli")
        else:
            rng = random.SystemRandom()
            p, q = rng.sample(pula, 2)
            return p, q

    elif nazwa == "G3":
        rng = random.Random(int(time.time()))

    elif nazwa == "G4":
        rng = random.SystemRandom()

    elif nazwa == "FERMAT": #mozna sprawdzic jak dalekie powinny byc p i q
        rng = random.SystemRandom()
        p = losuj_pierwsza(rng, k)
        q = p + 2
        while not czy_pierwsza_mr(q): q += 2
        return p, q

    else: raise ValueError("nieznany generator: " + nazwa)

    p = losuj_pierwsza(rng, k)
    q = losuj_pierwsza(rng, k)
    return p, q


