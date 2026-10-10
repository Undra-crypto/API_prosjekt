import os

import keyring
import requests
from dotenv import load_dotenv

load_dotenv()


def hent_nokkel() -> str:
    """Henter API-nøkkelen fra keyring, ellers fra .env."""
    nokkel = keyring.get_password("openweathermap", "api-key")
    if not nokkel:
        nokkel = os.getenv("OPENWEATHERMAP_API_KEY", "")
    return nokkel


def hent_koordinater(by: str, nokkel: str):
    """API 1: OpenWeatherMap geokoding (krever nøkkel)."""
    svar = requests.get(
        "https://api.openweathermap.org/geo/1.0/direct",
        params={"q": f"{by},NO", "limit": 1, "appid": nokkel},
        timeout=10,
    )
    if svar.status_code == 200:
        data = svar.json()
        if len(data) > 0:
            return data[0]["lat"], data[0]["lon"]
        print(f"Fant ingen treff for {by}")
    elif svar.status_code == 429:
        print("For mange forespørsler (rate limit)")
    else:
        print(f"Feil for {by}: statuskode {svar.status_code}")
    return None


def hent_soltider(lat: float, lon: float):
    """API 2: Sunrise-Sunset v2 (ingen nøkkel)."""
    svar = requests.get(
        "https://api.sunrise-sunset.org/v2",
        params={"lat": lat, "lng": lon},
        timeout=10,
    )
    if svar.status_code == 200:
        return svar.json()
    if svar.status_code == 429:
        print("For mange forespørsler til Sunrise-Sunset (rate limit)")
    else:
        print(f"Feil fra Sunrise-Sunset: statuskode {svar.status_code}")
    return None


def main():
    nokkel = hent_nokkel()
    if not nokkel:
        print("Fant ikke API-nøkkelen. Sjekk keyring eller .env.")
        return

    byer: list[str] = ["Hønefoss", "Oslo", "Trondheim"]
    for by in byer:
        koord = hent_koordinater(by, nokkel)
        if koord is None:
            continue
        lat, lon = koord
        tider = hent_soltider(lat, lon)
        if tider and tider.get("sunrise") and tider.get("sunset"):
            # ISO 8601 i lokal tid, f.eks. 2026-10-08T07:12:34+02:00
            opp = tider["sunrise"][11:16]
            ned = tider["sunset"][11:16]
            print(f"{by}: soloppgang {opp}, solnedgang {ned} (lokal tid)")


if __name__ == "__main__":
    main()