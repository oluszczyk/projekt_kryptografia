# 1. Instalacja narzędzi (winget)
winget install Git.Git
winget install Python.Python.3.12
winget install --id ShiningLight.OpenSSL.Light -e

# 2. Weryfikacja instalacji
git --version
python --version

# 3. Środowisko wirtualne i zależności
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# 4. Konfiguracja zmiennych środowiskowych OpenSSL
$openssl = "C:\Program Files\OpenSSL-Win64\bin"
$env:Path += ";$openssl"

# 4.5.
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";$openssl", "User")

# 5. Obsługa skryptu (Generowanie i Atak)
python cli.py generate --generator G2 --count 20 --bits 512 --out zestawy_g2/
python cli.py attack --in_dir zestawy_g2/ --out_dir zlamane_g2/

# 6. Ręczna weryfikacja złamanego klucza w OpenSSL
cd zlamane_g2
openssl rsa -in klucz_0000_priv.pem -text -noout
