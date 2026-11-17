"""pem_utils.py - wczytywanie kluczy z PEM i zapis odzyskanych kluczy prywatnych.

Wymaga: pip install pycryptodome
"""
from pathlib import Path

from Crypto.PublicKey import RSA

from attacks import break_keys


def load_public_pem(path):
    """Wczytuje klucz publiczny z pliku PEM i zwraca (N, e)."""
    key = RSA.import_key(Path(path).read_bytes())
    return key.n, key.e


def load_dir(directory):
    """Wczytuje wszystkie pliki *.pem z katalogu.

    Zwraca (nazwy_plikow, lista_N, e).
    """
    files = sorted(Path(directory).glob("*.pem"))
    names, moduli, e = [], [], 65537
    for f in files:
        n, e = load_public_pem(f)
        names.append(f.name)
        moduli.append(n)
    return names, moduli, e


def private_pem(n, e, d, p, q):
    """Sklada klucz prywatny z (N, e, d, p, q) i zwraca go jako PEM (bytes)."""
    # pycryptodome sprawdza spojnosc (p*q == N, e*d == 1 mod phi)
    key = RSA.construct((n, e, d, p, q))
    return key.export_key("PEM")


def break_dir(directory, out_dir):
    """Atak NWD na wszystkie klucze z katalogu.

    Dla zlamanych kluczy zapisuje odzyskany klucz prywatny jako
    <nazwa>_priv.pem w out_dir. Zwraca liczbe zlamanych kluczy.
    """
    names, moduli, e = load_dir(directory)
    broken = break_keys(moduli, e)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for idx, (p, q, d) in broken.items():
        pem = private_pem(moduli[idx], e, d, p, q)
        (out / f"{Path(names[idx]).stem}_priv.pem").write_bytes(pem)
    print(f"Zlamano {len(broken)} z {len(moduli)} kluczy")
    return len(broken)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("uzycie: python pem_utils.py <katalog_z_kluczami_pub> <katalog_wyjsciowy>")
        raise SystemExit(1)
    break_dir(sys.argv[1], sys.argv[2])