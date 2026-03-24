# 🎯 MatchVision - Začínáme Hned!

Vítejte! Toto je váš první soubor. Čtěte po pořadí! 👇

---

## ✨ Co máte

Komplět full-stack webovou aplikaci pro sledování fotbalových zápasů:

```
🏠 Domovská stránka → Jaké zápasy se teď hrají?
🔍 Vyhledávání → Najděte svůj oblíbený tým
⭐ Oblíbené → Sledujte své týmy
📊 Statistiky → Porovnujte týmy, grafyusement
🤖 AI Shrnutí → Čtěte automatické shrnutí zápasů
🔐 Bezpečný účet → Přihlaste se a ukládejte data
```

---

## ⚡ Spustit v 3 krocích (Windows)

### 1️⃣ Otevřete Command Prompt a jděte do složky

```cmd
cd C:\Users\georg\OneDrive\Plocha\TP\MatchVision
```

### 2️⃣ Instalace (první vez - trvá 2-3 minuty)

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Měli byste vidět `(venv)` na začítku řádky.

### 3️⃣ Spuštění

```cmd
python init_db.py
python run.py
```

Otevřete: **http://localhost:5000** 🎉

---

## 📖 Dokumentace (čtěte v tomto pověřoví)

| Soubor | Pro koho |
|--------|----------|
| **PROJECT_SUMMARY.md** | 📋 Přehled co máte |
| **QUICKSTART.md** | 🚀 Rychlý start (5 minut) |
| **WINDOWS_SETUP.md** | 🪟 Detailník nastavení na Windows |
| **README.md** | 📚 Úplná dokumentace |
| **ARCHITECTURE.md** | 🏗️ Jak je aplikace stavěna |
| **DEPLOY.md** | 🌐 Nasazení na Render |

---

## 🔑 Důležité soubory

```
.env                    ← UPRAVTE! Přidejte API klíč

app/
├── __init__.py        ← App factory (vytváří Flask)
├── config.py          ← Konfigurace
├── models/            ← User, FavoriteTeam (DB tabulky)
├── services/          ← API + AI logika
├── blueprints/        ← Routy (stránky)
├── templates/         ← HTML soubory
└── static/            ← CSS, JavaScript

run.py                 ← Spustit aplikaci: python run.py
init_db.py             ← Vytvořit DB: python init_db.py
seed_db.py             ← Demo data: python seed_db.py
test_app.py            ← Testy: python test_app.py
```

---

## 🎈 Prvních 10 minut

### 1. Spusťte aplikaci
```cmd
python run.py
```

### 2. Otevřete http://localhost:5000

### 3. Vyzkoušejte:
- ✅ Zobrazení domovské stránky
- ✅ Vyhledávání týmu (Vyhledávání → Manchester)
- ✅ Registrace (Registrovat se → vytvořit účet)
- ✅ Přihlášení (démó uživatel: demo / demo123)
- ✅ Přidání do oblíbených (❤️ na deatilu týmu)
- ✅ Zobrazení zápasu (detail s AI shrnutím)

---

## 🔴 Pokud něco nefunguje

### ❌ "python: command not found"
Máte Python? Stáhněte: https://www.python.org/downloads/

### ❌ "API not configured"
1. Otevřete `.env`
2. Přidejte API klíč z RapidAPI: https://rapidapi.com/api-football/api/api-football

### ❌ Port 5000 je zaneprázdněn
```cmd
python run.py --port 5001
```

### ❌ Databáze chyby
```cmd
del matchvision.db
python init_db.py
```

**❌ Pořád problém?** → Přečtěte si `WINDOWS_SETUP.md`

---

## 🎮 Demo Účet

Pokud jste spustili `python seed_db.py`:

```
Email: demo@matchvision.com
Heslo: demo123
```

Nebo si vytvořte svůj vlastní účet!

---

## 🌐 Nasazení Online (Render)

Jakmile má vše běžet lokálně:

1. Push na GitHub: `git push`
2. Render.com - VyberteRepositář
3. Deploy!

Viz `DEPLOY.md` pro detaily.

---

## 📁 Struktura Projektu

```
MatchVision/
├── app/                    # Hlavní aplikace
│   ├── blueprints/         # Routy (stránky)
│   ├── models/             # Databázové tabulky
│   ├── services/           # API + Business logika
│   ├── static/             # CSS, JavaScript
│   └── templates/          # HTML šablony
│
├── run.py                  # Spustit aplikaci
├── requirements.txt        # Závislosti (pip install)
├── .env                    # Konfigurace (NEpushovat!)
│
└── Dokumentace/
    ├── README.md           # Úplná dokumentace
    ├── QUICKSTART.md       # Rychlý start
    ├── ARCHITECTURE.md     # Jak je stavěna
    └── DEPLOY.md           # Nasazení
```

---

## 🎓 Naučte se kód

1. **Frontend** - `app/templates/*.html` + `app/static/`
   - HTML struktura
   - Bootstrap 5 třídy
   - JavaScript funkce

2. **Backend** - `app/blueprints/*.py`
   - Flask routy
   - Database queries
   - API volání

3. **Databáze** - `app/models/db_models.py`
   - SQLAlchemy modely
   - Relace

4. **API** - `app/services/api_service.py`
   - RapidAPI integrace
   - HTTP requesty

5. **AI** - `app/services/summary_service.py`
   - Logické generování textu
   - Template-based approach

---

## 💡 Komentáře v Kódu

Každý soubor má komentáře! Např:

```python
# auth.py
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user"""  # <-- Komentář vysvětluje funkci
    # ... kód ...
```

Čtěte kód a učte se! 📚

---

## 🚀 Příští Kroky

### 📈 Rozšíření aplikace
- Přidejte více funcialit
- Upravte design
- Přidejte fotbal data
- Vytvořte bot

### 🌐 Nasazení
- Push na GitHub
- Deploy na Render
- Sdílejte s přáteli

### 📚 Učit se
- Čtěte Flask docs
- Zkoumejte SQLAlchemy
- Experimentujte s kodem

---

## 📞 Kde Hledat Pomoc

1. **Chyba?** → Čtěte logy (Command Prompt)
2. **Nejasno?** → Čtěte WINDOWS_SETUP.md
3. **Jak to funguje?** → ARCHITECTURE.md
4. **Jak nasadit?** → DEPLOY.md
5. **Všeobecné otázky?** → README.md

---

## ✅ Checklist

- [ ] Spusťte `python run.py`
- [ ] Otevřete http://localhost:5000
- [ ] Zaregistrujte se
- [ ] Vyhledajte tým
- [ ] Přidat do oblíbených
- [ ] Přečtěte README.md
- [ ] Podívejte se na kód v `app/`
- [ ] Upravte design v `style.css`
- [ ] Pushujte na GitHub
- [ ] Deployujte na Render
- [ ] Sdílejte s přáteli! 🎉

---

## 🎯 Vaše cesta k learnim

```
1. Teď                    ← Jste tady
2. Číst QUICKSTART.md     ← Příští krok
3. Spustit aplikaci       ← Běžel kód
4. Prozkoumat kód         ← Porozumět designu
5. Upravit design         ← Tvořit
6. Přidat funkcionalitu   ← Vyvíjet
7. Nasadit online         ← Sdílet
8. Oslava! 🎉             ← Úspěch
```

---

## 🎊 Hurá!

Máte kompletní, profesionální webovou aplikaci!

Následující je co nyní:

1. **Místní test**: `python run.py`
2. **Prozkoumat**: Čtěte `app/` složku
3. **Učit se**: Čtěte dokumentaci
4. **Vylepšovat**: Přidejte své nápady
5. **Sdílet**: Deploy na Render

---

**Hodně štěstí! ⚽**

Zkuste si to! Aplikace je připravená a fungující.

Máte otázky? Všechna odpovědi jsou v dokumentaci.

👉 **Příští:** Čtěte `QUICKSTART.md` nebo `WINDOWS_SETUP.md`
