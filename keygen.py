import random
import math
import os
from generators import generator
from generators import stworz_pule
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

rng = random.Random(124)

def generuj_klucz(nazwa, bity, ziarno=None, pula=None):
    k = bity//2
    p, q = generator(nazwa, k, ziarno, pula)
    e = 65537


    while(p == q or math.gcd((p-1)*(q-1), e) != 1):
        p, q = generator(nazwa, k, ziarno, pula)

    phi = (p-1)*(q-1)
    n = p*q
    d = pow(e, -1, phi)

    return {"n": n, "e": e, "d": d, "p": p, "q": q}

def zapisz_pem(klucz, nazwa_pliku):
    n, e, d, p, q = klucz["n"], klucz["e"], klucz["d"], klucz["p"], klucz["q"]
 
    dmp1 = rsa.rsa_crt_dmp1(d, p)
    dmq1 = rsa.rsa_crt_dmq1(d, q)
    iqmp = rsa.rsa_crt_iqmp(p,q) #pomocnicze do klucza

    publiczne = rsa.RSAPublicNumbers(e, n)
    prywatne = rsa.RSAPrivateNumbers(p, q, d, dmp1, dmq1, iqmp, publiczne)
    obiekt = prywatne.private_key()

    #zamiana na PEM
    dane = obiekt.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    with open(nazwa_pliku, "wb") as f:
        f.write(dane)

def generuj_zestaw(nazwa, bity, ile, folder, rozmiar_puli=None):
    os.makedirs(folder, exist_ok=True)

    pula = None
    if nazwa == "G2":
        pula = stworz_pule(bity // 2, rozmiar_puli)

    klucze = []
    for i in range(ile):
        klucz = generuj_klucz(nazwa, bity, pula=pula)
        sciezka = os.path.join(folder, f"klucz_{i:04d}.pem")
        zapisz_pem(klucz, sciezka)
        klucze.append(klucz)

    return klucze

if __name__ == "__main__":
    generuj_zestaw("G1", 512, 10, "testowa_pula")

    #print(losuj_pierwsza(rng, 512))

    #print(generuj_klucz(rng, 512))

    #klucz = generuj_klucz(rng, 512)
    #print(klucz["n"].bit_length())              # ma być 512
    #m = 42
    #c = pow(m, klucz["e"], klucz["n"])
    #print(c)                                    # szyfrogram: wielka, „losowa" liczba
    #print(pow(c, klucz["d"], klucz["n"]))       # ma wrócić 42

    #klucz = generuj_klucz(rng, 1024)
    #zapisz_pem(klucz, "test.pem")

    """
    pula = stworz_pule(512, 10)
    klucze = []

    for _ in range(20):
        klucze.append(generuj_klucz("G2", 1024, pula=pula))
    
    #slabosc G2
    ile = 0
    for i in range(0, len(klucze)):
        for j in range(i+1, len(klucze)):
            w = math.gcd(klucze[i]["n"], klucze[j]["n"])
            if w > 1:
                ile += 1
                print("klucze ", i, " oraz ", j)

    print(ile)
    """

    """
    #sprawdzenie G1 (takie samo ziarno)
    k1 = generuj_klucz("G1", 512, 1234)
    k2 = generuj_klucz("G1", 512, 1234)
    k3 = generuj_klucz("G1", 512, 1235)

    if k1["n"] == k2["n"]: print("OK")
    else: print("blad") 

    if k1["n"] != k3["n"]: print("OK")
    else: print("blad") 
    """

    #zapisz_pem(generuj_klucz("FERMAT", 512), "test_fermat.pem")

    
