# API_prosjekt

Python-program som henter data fra to API-er:

1. **OpenWeatherMap Geocoding** (krever API-nøkkel): henter koordinater for byer
2. **Sunrise-Sunset** (ingen nøkkel): henter soloppgang og solnedgang for koordinatene

Programmet skriver ut soloppgang og solnedgang (lokal tid) for Hønefoss, Oslo og Trondheim.

## Slik kjører dere programmet

1. Skaff deres egen gratis API-nøkkel på https://openweathermap.org/api
2. Lag og aktiver et virtuelt miljø:
   - `python -m venv .venv`
   - Windows: `.venv\Scripts\Activate.ps1`
3. Installer pakkene: `pip install -r requirements.txt`
4. Lagre nøkkelen på ÉN av to måter:
   - **keyring:** `python -m keyring set openweathermap api-key`
   - **.env:** kopier `.env.example` til `.env` og fyll inn nøkkelen etter `=`
5. Kjør: `python main.py`

Nøkkelen ligger aldri i koden eller på GitHub. `.env` er ignorert via `.gitignore`.

Soltider fra [Sunrise-Sunset.org](https://sunrise-sunset.org).