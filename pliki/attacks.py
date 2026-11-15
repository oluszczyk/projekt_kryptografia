"""attacks.py - etap 2: atak NWD parami + odtwarzanie klucza prywatnego.

Atak dziala na WLASNYCH kluczach testowych wygenerowanych slabym generatorem
(G2 - mala pula liczb pierwszych). Jesli dwa moduly maja wspolna liczbe
pierwsza p, to NWD(N1, N2) = p i oba klucze da sie rozlozyc.
"""
from math import gcd
from itertools import combinations


def gcd_pairs(moduli):
    """Dla kazdej pary modulow liczy NWD.

    Zwraca liste krotek (i, j, p), gdzie p = NWD(N_i, N_j) > 1.
    Pary z p == N (identyczne moduly) pomijamy - to nie daje rozkladu.
    """
    found = []
    for i, j in combinations(range(len(moduli)), 2):
        p = gcd(moduli[i], moduli[j])
        if 1 < p < moduli[i] and p < moduli[j]:
            found.append((i, j, p))
    return found


def recover_private_key(n, e, p):
    """Majac N, e i jeden czynnik p, odtwarza p, q, phi(N) oraz d."""
    if n % p != 0:
        raise ValueError("p nie dzieli N")
    q = n // p
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)  # odwrotnosc e modulo phi(N)
    return p, q, d


def break_keys(moduli, e=65537):
    """Lamie wszystkie klucze, ktore maja wspolny czynnik z innym kluczem.

    Zwraca slownik {indeks_klucza: (p, q, d)}.
    """
    broken = {}
    for i, j, p in gcd_pairs(moduli):
        for idx in (i, j):
            if idx not in broken:
                broken[idx] = recover_private_key(moduli[idx], e, p)
    return broken


def check_key(n, e, d, message=42):
    """Sprawdza, czy odzyskany klucz dziala: szyfruje kluczem publicznym,
    odszyfrowuje odzyskanym d."""
    c = pow(message, e, n)
    return pow(c, d, n) == message


# ---------------------------------------------------------------------------
# Przyklad na malych liczbach (do prezentacji na etapie 2)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    e = 65537
    # N1 = p*q1, N2 = p*q2, N3 = zupelnie inne liczby pierwsze
    p, q1, q2 = 10007, 10009, 10037
    r, s = 10069, 10079
    moduli = [p * q1, p * q2, r * s]

    print("Moduly:", moduli)
    print("Wspolne czynniki (i, j, NWD):", gcd_pairs(moduli))

    for idx, (pp, qq, d) in break_keys(moduli, e).items():
        n = moduli[idx]
        print(f"Klucz {idx}: N={n} = {pp} * {qq}, d={d}, "
              f"dziala: {check_key(n, e, d)}")

    # klucz nr 2 nie ma wspolnego czynnika - atak go nie zlamie
    print("Klucz 2 zlamany?", 2 in break_keys(moduli, e))