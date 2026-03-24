# MatchVision - Quick Start Guide

## 🚀 Rychlý Start (5 minut)

### Krok 1: Příprava
```bash
# Klonujte/stáhněte projekt
cd MatchVision

# Vytvořte virtuální prostředí
python -m venv venv

# Aktivujte virtuální prostředí
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalujte závislosti
pip install -r requirements.txt
```

### Krok 2: Konfigurace
```bash
# Zkopírujte .env.example na .env
cp .env.example .env

# Editujte .env a přidejte API klíč (DŮLEŽITÉ!)
# Získejte API klíč zde: https://rapidapi.com/api-football/api/api-football
```

**`.env` - Příklad:**
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-12345
DATABASE_URL=sqlite:///matchvision.db
API_FOOTBALL_KEY=váš_api_klíč_zde
```

### Krok 3: Inicializace databáze
```bash
python init_db.py
```

Výstup:
```
Vytvářím databázi...
✅ Databáze vytvořena úspěšně!

Vytvořené tabulky: 2
  - users
  - favorite_teams
```

### Krok 4: (Volitelné) Seedování demo dat
```bash
python seed_db.py
```

Demo účet:
- **Username**: demo
- **Heslo**: demo123

### Krok 5: Spuštění aplikace
```bash
python run.py
```

Otevřete v prohlížeči: **http://localhost:5000**

---

## 🧪 Kontrola funkčnosti

```bash
python test_app.py
```

Tento skript ověří:
- ✅ Vytvoření aplikace
- ✅ Konfigurace
- ✅ Databázi
- ✅ Modely
- ✅ Blueprinty
- ✅ API klíč

---

## 📝 Prvních kroků v aplikaci

1. **Registrujte nový účet** - Přejděte na "Registrovat se"
2. **Vyhledejte tým** - Přejděte na "Vyhledávání"
3. **Přidejte do oblíbených** - Klikněte "Přidat do oblíbených"
4. **Sledujte živé zápasy** - Na domovské stránce vidíte aktuální zápasy

---

## 🔧 Běžné problémy

### "ModuleNotFoundError: No module named 'flask'"
```bash
# Zapomínáte aktivovat virtuální prostředí!
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Poté znovu spusťte:
pip install -r requirements.txt
```

### "API not configured"
```bash
# Přidejte API klíč do .env
API_FOOTBALL_KEY=váš_klíč_z_RapidAPI
```

### "Database is locked"
```bash
# Smažte matchvision.db a vytvořte znovu
rm matchvision.db  # Linux/macOS
del matchvision.db # Windows

python init_db.py
```

### "Port 5000 is already in use"
```bash
# Spusťte na jiném portu
python run.py --port 5001
```

---

## 📂 Struktura projektů

```
MatchVision/
├── app/                    # Hlavní aplikace
│   ├── blueprints/         # Flask Blueprints (routy)
│   ├── models/             # Databázové modely
│   ├── services/           # API + Business logika
│   ├── static/             # CSS + JS
│   └── templates/          # HTML šablony
├── run.py                  # Spuštění aplikace
├── init_db.py              # Inicializace DB
├── seed_db.py              # Demo data
├── test_app.py             # Testy
├── requirements.txt        # Závislosti
└── .env                    # Konfigurace (NEpushujte!)
```

---

## 🚢 Nasazení na Render

### Příprava
1. Pushujte kód na GitHub
2. Přejděte na [render.com](https://render.com)
3. Vyberte "New Web Service"
4. Vyberte váš GitHub repozitář

### Konfigurace v Render
| Nastavení | Hodnota |
|-----------|---------|
| **Name** | MatchVision |
| **Environment** | Python |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn run:app` |
| **Python Version** | 3.9 |

### Environment Variables
Přidejte v nastavení:
```
FLASK_ENV=production
SECRET_KEY=váš-bezpečný-klíč-min-32-znaků
API_FOOTBALL_KEY=váš-api-klíč
DATABASE_URL=sqlite:///matchvision.db
```

### Deploy
Klikněte "Deploy" a čekejte! 🚀

Vaše aplikace bude dostupná na:
```
https://matchvision-xxxxx.onrender.com
```

---

## 📚 Užitečné knihy

- [Flask Official Docs](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.0/)
- [Chart.js Documentation](https://www.chartjs.org/)

---

## 💡 Tipy

- Používejte `.env` pro citlivé údaje
- Vytvářejte commits po každé funkci
- Testujte aplikaci lokálně předtím, než pushujete
- Čtěte logy pro debug

---

## 🤝 Contribuce

Našli jste bug? Máte nápad na vylepšení?

1. Fork projekt
2. Vytvořte feature branch (`git checkout -b feature/amazing-feature`)
3. Commitujte změny (`git commit -m 'Add amazing feature'`)
4. Pushujte na branch (`git push origin feature/amazing-feature`)
5. Otevřete Pull Request

---

## 📄 Licence

Projekt je vyvíjen pro vzdělávací účely.

---

**Hodně štěstí! ⚽** Pokud máte otázky, koukněte na README.md nebo se podívejte na kód.
