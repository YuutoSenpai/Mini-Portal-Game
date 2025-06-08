# Mini Portal Game

2D logická hra inspirovaná Portalem, vytvořená pomocí Pygame.

## Funkce

* **Portálová mechanika**: Vytvářej modré a oranžové portály pro teleportaci mezi částmi úrovně
* **11 náročných úrovní**: Od výukových po pokročilé hádanky
* **Hra založená na fyzice**: Realistický pohyb a přenášení hybnosti skrz portály
* **Systém ukládání**: Více uložených pozic a sledování postupu
* **Hodnocení hvězdami**: Časové skóre pro každou úroveň
* **Plná podpora myši a klávesnice**: Kompletní ovládání menu
* **Zvukový systém**: Procedurální zvuky a hudba na pozadí
* **Systém nápovědy**: Automatické zobrazování tipů a možnost je zapínat/vypínat ručně

## Ovládání

* **Pohyb**: WASD nebo šipky
* **Skok**: Mezerník
* **Modrý portál**: Levé tlačítko myši
* **Oranžový portál**: Pravé tlačítko myši
* **Restart úrovně**: R
* **Pauza / Menu**: ESC
* **Přepnutí nápovědy**: H
* **Celá obrazovka**: F11

## Instalace

### Možnost 1: Připraveno k hraní (doporučeno)

Hra obsahuje přednastavené virtuální prostředí se všemi závislostmi:

**Linux/Mac:**

```bash
./run_game.sh
```

**Windows:**

```bash
run_game.bat
```

### Možnost 2: Ruční instalace

Pokud si chceš závislosti nainstalovat sám:

1. Nainstaluj Python 3.7+ a potřebné balíčky:

   ```bash
   pip install pygame numpy
   ```

2. Spusť hru:

   ```bash
   python main.py
   ```

## Struktura projektu

```
Mini-Portal-Game/
├── main.py                 # Hlavní spouštěcí soubor hry
├── run_game.sh            # Spouštěč pro Linux/Mac
├── run_game.bat           # Spouštěč pro Windows
├── requirements.txt       # Seznam závislostí
├── README.md              # Tento soubor
├── game/                  # Hlavní herní balík
│   ├── core/              # Jádro herních systémů
│   │   ├── game.py        # Hlavní logika hry
│   │   ├── player.py      # Postava hráče
│   │   ├── portal.py      # Portálová mechanika
│   │   ├── game_objects.py # Krabice, přepínače, cíle
│   │   ├── camera.py      # Kamerový systém
│   │   └── effects.py     # Vizuální efekty
│   ├── levels/            # Generování úrovní
│   │   └── level.py       # Definice úrovní
│   ├── ui/                # Uživatelské rozhraní
│   │   ├── ui.py          # Herní UI prvky
│   │   └── sound_manager.py # Zvukový systém
│   ├── utils/             # Pomocné funkce
│   │   └── constants.py   # Herní konstanty
│   └── main_game.py       # Řízení hlavní hry
└── data/                  # Herní data
    ├── venv/              # Virtuální prostředí Pythonu
    ├── saves/             # Uložené pozice
    └── settings/          # Nastavení
```

## Herní princip

Procházej stále složitější úrovně pomocí portálové mechaniky:

1. **Výukové úrovně** (0–2): Základy umisťování portálů
2. **Logické úrovně** (3–5): Použití krabic a přepínačů
3. **Pokročilé úrovně** (6–8): Výzvy na hybnost a přesnost
4. **Závěrečné úrovně** (9–10): Kombinace všech herních mechanik

Získávej hvězdy podle času dokončení a pokus se získat všechny!

## Licence

Vytvořeno jako školní projekt. Inspirováno hrou Portal (Valve Corporation).
