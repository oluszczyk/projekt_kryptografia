#wystarczy pow(e, -1, phi)
import math

def odw(e, phi):
    stare_r, r = phi, e
    stare_t, t = 0, 1

    while r != 0:
        q = stare_r // r
        stare_r, r = r, stare_r - q * r
        stare_t, t = t, stare_t - q * t
        print("q =", q, "| reszty:", stare_r, r, "| siódemki:", stare_t, t)

    return stare_t % phi

print(odw(17, 40))