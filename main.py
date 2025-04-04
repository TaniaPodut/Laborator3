import json
import random

def citeste_datele(path):
    with open(path, 'r') as f:
        return json.load(f)

def calculeaza_rest(rest, bancnote):
    """
    Programare Dinamică cu stoc limitat.
    Returnează: dict {valoare_bancnotă: număr}, sau None dacă nu se poate da restul.
    """
    dp = [None] * (rest + 1)
    dp[0] = {}

    for i in range(1, rest + 1):
        for b in bancnote:
            val = b["valoare"]
            stoc = b["stoc"]
            if val > i:
                continue
            for k in range(1, stoc + 1):
                prev = i - k * val
                if prev < 0 or dp[prev] is None:
                    continue
                candidat = dp[prev].copy()
                candidat[val] = candidat.get(val, 0) + k
                total_bancnote = sum(candidat.values())
                if dp[i] is None or total_bancnote < sum(dp[i].values()):
                    dp[i] = candidat
    return dp[rest]

def actualizeaza_stoc(rest_bancnote, bancnote):
    for val, cant in rest_bancnote.items():
        for b in bancnote:
            if b["valoare"] == val:
                b["stoc"] -= cant
                break

def format_bancnote(rest_bancnote):
    bucati = []
    for val in sorted(rest_bancnote.keys(), reverse=True):
        nr = rest_bancnote[val]
        text_b = "bancnotă" if nr == 1 else "bancnote"
        total_valoare = val * nr
        moneda = "leu" if total_valoare == 1 else "lei"
        bucati.append(f"{val} {moneda} – {nr} {text_b}")
    return ", ".join(bucati)

def simuleaza(path):
    data = citeste_datele(path)
    bancnote = data["bancnote"]
    produse = data["produse"]
    client_id = 1

    while True:
        produs = random.choice(produse)
        pret = produs["pret"]
        suma_platita = random.randint(pret + 1, pret + 20)
        rest = suma_platita - pret

        print(f"\nClient #{client_id}")
        print(f"Produs cumpărat: {produs['nume']}")
        print(f"Preț: {pret} lei")
        print(f"Suma plătită: {suma_platita} lei")
        print(f"Rest de oferit: {rest} lei")

        rest_bancnote = calculeaza_rest(rest, bancnote)

        if rest_bancnote is None:
            print("️Nu se poate oferi restul cu bancnotele disponibile.")
            break
        else:
            print("Restul oferit (și cu ce bancnote):", format_bancnote(rest_bancnote))
            actualizeaza_stoc(rest_bancnote, bancnote)

        client_id += 1

# Rularea simulării
simuleaza('date.json')
