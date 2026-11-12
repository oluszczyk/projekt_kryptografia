
def NWD(a, b):
    while(b):
        r = a%b
        a = b
        b = r

    return a



#print(NWD(391, 493)) śmiga, mozna krocej a, b = b, a%b
#skorzystamy z import math  math.gcd(391, 493) jest szybsza
