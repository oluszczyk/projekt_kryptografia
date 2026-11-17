"""Testy poprawnosci ataku NWD (uruchom: pytest -v)."""
import shutil
import subprocess

import pytest
from Crypto.PublicKey import RSA
from Crypto.Util.number import getPrime

from attacks import break_keys, check_key, gcd_pairs
from pem_utils import break_dir

E = 65537


def make_moduli(bits=512):
    """Trzy klucze testowe: pierwsze dwa maja wspolne p, trzeci jest niezalezny."""
    while True:
        p, q1, q2, r, s = (getPrime(bits) for _ in range(5))
        if len({p, q1, q2, r, s}) == 5:
            break
    return [p * q1, p * q2, r * s], p


def test_finds_shared_prime():
    moduli, p = make_moduli()
    assert gcd_pairs(moduli) == [(0, 1, p)]


def test_breaks_only_keys_with_shared_prime():
    moduli, _ = make_moduli()
    broken = break_keys(moduli, E)
    assert set(broken) == {0, 1}


def test_recovered_key_decrypts():
    moduli, _ = make_moduli()
    for idx, (p, q, d) in break_keys(moduli, E).items():
        assert p * q == moduli[idx]
        assert check_key(moduli[idx], E, d)


def test_no_shared_primes_nothing_broken():
    # klucze z "dobrego" generatora: brak wspolnych czynnikow
    moduli = [getPrime(256) * getPrime(256) for _ in range(5)]
    assert break_keys(moduli, E) == {}


@pytest.mark.skipif(shutil.which("openssl") is None, reason="brak OpenSSL")
def test_openssl_accepts_recovered_key(tmp_path):
    moduli, _ = make_moduli()
    pub_dir, out_dir = tmp_path / "pub", tmp_path / "out"
    pub_dir.mkdir()
    for i, n in enumerate(moduli):
        (pub_dir / f"key{i}.pem").write_bytes(RSA.construct((n, E)).export_key("PEM"))

    assert break_dir(pub_dir, out_dir) == 2

    for f in out_dir.glob("*_priv.pem"):
        res = subprocess.run(["openssl", "rsa", "-in", str(f), "-check", "-noout"],
                             capture_output=True, text=True)
        assert "RSA key ok" in res.stdout, res.stderr