import argparse
from keygen import generuj_zestaw
from pem_utils import break_dir

def main():
    parser = argparse.ArgumentParser(description="Projekt: Wpływ PRNG na bezpieczeństwo kluczy RSA")
    subparsers = parser.add_subparsers(dest="command", help="Dostępne komendy")

    # --- Podkomenda: generate ---
    parser_gen = subparsers.add_parser("generate", help="Generowanie zestawu kluczy RSA")
    parser_gen.add_argument("--generator", type=str, choices=["G1", "G2", "G3", "G4", "FERMAT"], required=True)
    parser_gen.add_argument("--count", type=int, default=10, help="Liczba kluczy")
    parser_gen.add_argument("--bits", type=int, default=1024, choices=[512, 1024, 2048])
    parser_gen.add_argument("--out", type=str, default="zestawy/", help="Katalog wyjściowy")
    parser_gen.add_argument("--pool", type=int, default=50, help="Rozmiar puli (tylko dla G2)")

    # --- Podkomenda: attack ---
    parser_attack = subparsers.add_parser("attack", help="Atakowanie kluczy (domyślnie NWD)")
    parser_attack.add_argument("--in_dir", type=str, default="zestawy/", help="Katalog z kluczami do ataku")
    parser_attack.add_argument("--out_dir", type=str, default="zlamane/", help="Katalog na odzyskane klucze prywatne")

    args = parser.parse_args()

    if args.command == "generate":
        print(f"[*] Generowanie {args.count} kluczy ({args.bits} bitów) generatorem {args.generator}...")
        generuj_zestaw(args.generator, args.bits, args.count, args.out, rozmiar_puli=args.pool)
        print(f"[+] Zapisano do {args.out}")

    elif args.command == "attack":
        print(f"[*] Rozpoczynam atak NWD na klucze w katalogu {args.in_dir}...")
        broken_count = break_dir(args.in_dir, args.out_dir)
        print(f"[+] Zakończono. Zapisano odzyskane klucze w {args.out_dir}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()