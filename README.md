# MatchVision - Fotbalová webová aplikace

Kompletní full-stack webová aplikace pro sledování fotbalových zápasů v reálném čase s AI shrnutím, statistikami a grafy.

## Technologický stack

### Backend
- **Python 3** s **Flask** micro-framework
- **SQLAlchemy ORM** pro práci s databází
- **Flask-Login** pro autentizaci
- **Flask-WTF** pro formuláře a CSRF ochranu
- **Werkzeug** pro hashování hesel

### Frontend
- **HTML5** + **Bootstrap 5** pro responzivní design
- **Vanilla JavaScript** (bez závislostí)
- **Chart.js** pro grafy a vizualizace
- Tmavý, moderní design

### Databáze
- **SQLite** s jednoduchou migrací

### API
- **API-Football** (RapidAPI) pro fotbalové data

## Funkcionality

### 1. Autentizace
- ✅ Registrace nového uživatele
- ✅ Přihlášení/Odhlášení
- ✅ Bezpečné hashování hesel (bcrypt)
- ✅ Ochrana rout pro přihlášené uživatele
- ✅ Zapamatování přihlášení

### 2. Správa oblíbených týmů
- ✅ Přidávání/Odebírání týmů
- ✅ Zobrazení seznamu oblíbených
- ✅ Uložení v databázi

### 3. API integrace
- ✅ Živé zápasy (Live matches)
- ✅ Liga tabulky (League standings)
- ✅ Detail týmu s statistikami
- ✅ Detail zápasu se statistikami
- ✅ Vyhledávání týmů
- ✅ Nejnovější zápasy týmu
- ✅ Nadcházející zápasy

### 4. AI Shrnutí zápasu
- ✅ Generování shrnutí ze statistik
- ✅ Analýza: skóre, střely, držení míče, karty
- ✅ Profesionální text v češtině
- ✅ Bez externích AI API

### 5. Grafy a statistiky
- ✅ Forma týmu (poslední 5 zápasů)
- ✅ Srovnění dvou týmů
- ✅ Liga tabulky
- ✅ Interaktivní grafy (Chart.js)

### 6. Uživatelské rozhraní
- ✅ Tmavý, moderní design
- ✅ Responsivní layout (mobile-first)
- ✅ Intuitivní navigace
- ✅ Flash messages pro feedback
- ✅ Bootstrap 5 komponenty

## Instalace

### Požadavky
- Python 3.8+
- pip
- API klíč z [RapidAPI - API-Football](https://rapidapi.com/api-football/api/api-football)

### Lokální spuštění

1. **Klonování repozitáře**
```bash
cd MatchVision
```

2. **Vytvoření virtuálního prostředí**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. **Instalace závislostí**
```bash
pip install -r requirements.txt
```

4. **Konfigurace environment**
```bash
# Kopírování příkladu
cp .env.example .env

# Editujte .env a přidejte svůj API klíč
API_FOOTBALL_KEY=váš_api_klíč_zde
SECRET_KEY=váš_tajný_klíč_zde
```

5. **Spuštění aplikace**
```bash
python run.py
```

Aplikace bude dostupná na `http://localhost:5000`

## Nasazení na Render

### Příprava

1. **Vytvoření repozitáře na GitHubu**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <vaše-repo-url>
git push -u origin main
```

2. **Vytvoření Web Service na Render**
   - Jděte na [Render.com](https://render.com)
   - Klikněte "New +" → "Web Service"
   - Vyberte váš GitHub repozitář
   - Nastavte:
     - **Name**: MatchVision
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn run:app`
     - **Python Version**: 3.9

3. **Nastavení Environment Variables**
   - V sekci "Environment" přidejte:
     ```
     FLASK_ENV=production
     SECRET_KEY=váš-tajný-klíč
     API_FOOTBALL_KEY=váš-api-klíč
     DATABASE_URL=sqlite:///matchvision.db
     ```

4. **Deploy**
   - Klikněte "Deploy"
   - Čekejte na inicializaci databáze
   - Aplikace bude dostupná na `https://matchvision-<suffix>.onrender.com`

## Struktura projektu

```
MatchVision/
├── app/
│   ├── __init__.py           # App factory
│   ├── config.py             # Konfigurace
│   ├── models/
│   │   ├── __init__.py
│   │   └── db_models.py      # SQLAlchemy modely
│   ├── services/
│   │   ├── __init__.py
│   │   ├── api_service.py    # API-Football integrace
│   │   └── summary_service.py # Generování shrnutí
│   ├── blueprints/
│   │   ├── __init__.py
│   │   ├── auth.py           # Autentizace
│   │   ├── main.py           # Hlavní stránka
│   │   ├── teams.py          # Týmy
│   │   ├── matches.py        # Zápasy
│   │   └── favorites.py      # Oblíbené
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── auth/
│       ├── matches/
│       ├── teams/
│       └── favorites.html
├── run.py                    # Entry point
├── requirements.txt          # Závislosti
├── .env.example             # Příklad konfigurace
├── .gitignore
└── README.md
```

## API Endpoints

### Autentizace
- `GET/POST /auth/register` - Registrace
- `GET/POST /auth/login` - Přihlášení
- `GET /auth/logout` - Odhlášení

### Zápasy
- `GET /` - Domovská stránka
- `GET /matches/live` - Živé zápasy
- `GET /matches/<id>` - Detail zápasu
- `GET /matches/<id>/summary` - AI shrnutí

### Týmy
- `GET /teams/search` - Vyhledávání
- `GET /teams/<id>` - Detail týmu
- `POST /teams/<id>/favorite` - Přidat do oblíbených
- `DELETE /teams/<id>/favorite` - Odstranit z oblíbených
- `GET /teams/compare` - Porovnání

### Liga
- `GET /leagues` - Všechny ligy
- `GET /league/<id>` - Tabulka ligy

### Oblíbené
- `GET /favorites/` - Seznam oblíbených
- `GET /favorites/api` - API seznam (JSON)

## Databázový model

### Users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### FavoriteTeams
```sql
CREATE TABLE favorite_teams (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    team_name VARCHAR(120) NOT NULL,
    team_logo VARCHAR(500),
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    UNIQUE(user_id, team_id)
);
```

## Bezpečnost

- ✅ **Hashování hesel** - Werkzeug security
- ✅ **CSRF ochrana** - Flask-WTF
- ✅ **SQL Injection ochrana** - SQLAlchemy ORM
- ✅ **XSS ochrana** - Jinja2 auto-escaping
- ✅ **Autentizace** - Flask-Login
- ✅ **HTTPS** - Doporučeno pro production
- ✅ **Bezpečné cookies** - HttpOnly + Secure flags

## Konfigurace

### Environment Variables
```
FLASK_APP=run.py
FLASK_ENV=development|production
SECRET_KEY=váš-tajný-klíč-min-32-znaků
DATABASE_URL=sqlite:///matchvision.db
API_FOOTBALL_KEY=váš-api-klíč
```

### config.py
```python
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    API_FOOTBALL_KEY = os.getenv('API_FOOTBALL_KEY')
```

## Development

### Spuštění v debug módu
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py
```

### Spuštění testů (budoucí)
```bash
pytest
```

## Odpovědy na obvyklé otázky

**Q: Jak změním API klíč?**
A: Editujte `.env` soubor a přidejte svůj klíč z RapidAPI.

**Q: Aplikace zobrazuje chybu "API not configured"**
A: Zkontrolujte, že máte vyplněný `API_FOOTBALL_KEY` v `.env`.

**Q: Chci přidat další ligu**
A: Editujte `app/services/api_service.py` - funkci `get_top_leagues()` a přidejte ligu ID.

**Q: Mohu měnit barvy a design?**
A: Ano! Editujte `app/static/css/style.css` - všechny barvy jsou definovány v `:root`.

## Budoucí vylepšení

- [ ] Notifikace pro favorované týmy
- [ ] Statistiky uživatele (sledované zápasy)
- [ ] Tipování zápasů
- [ ] Push notifikace
- [ ] iOS/Android mobilní aplikace
- [ ] Admin panel
- [ ] Komentáře k zápasům
- [ ] Více jazyků (EN, DE, FR)

## Licenční ujednání

Tento projekt je vyvíjen pro vzdělávací účely. Używaní API-Football vyžaduje splnění jejich podmínek služby.

## Kontakt a podpora

Pro problémy a návrhy otevřete issue v GitHubu.

---

**MatchVision v2.0** - Vytvořeno v 2026 ⚽

Vytvořeno s ❤️ pro fotbalové nadšence
