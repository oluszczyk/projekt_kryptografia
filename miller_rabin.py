import random
import math

def rozloz(n):
    ile_dwojek=0
    np = n-1
    while(np%2 == 0):
        ile_dwojek +=1
        np //=2
    return ile_dwojek, np

def runda(n, a, s, d):
    x = pow(a, d, n)
    if x == 1 or x == n-1: return True

    for _ in range(s-1):
        x = pow(x, 2, n)
        if x == n-1: return True
        elif x == 1: return False
        s -= 1

    return False

def czy_pierwsza(n):
    if n < 2: return False
    elif n == 2: return True

    i=2
    while(i*i <= n):
        if n%i == 0: return False
        i+=1
    return True

def czy_pierwsza_mr(n, k=40):
    if n < 2: return False
    elif n == 2 or n == 3: return True
    elif n%2 == 0: return False

    s, d = rozloz(n)

    for _ in range(k):
        a = random.randrange(2, n-1) #n-1 nie wchodzi do zbioru
        if runda(n, a, s, d) == False: return False

    return True

def sprawdzenie_mr():
    s=0
    for i in range(2, 100000):
        if czy_pierwsza(i) != czy_pierwsza_mr(i): print("rozni sie dla ", i)
        else: s+=1
    print(s)

if __name__ == "__main__":
    sprawdzenie_mr()