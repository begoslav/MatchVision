# MatchVision - Architektura a Design

Komplexně popsaná architektura aplikace MatchVision.

## 🏗️ Architektura

```
┌─────────────────────────────────────────────────────────────┐
│                        Klient (Browser)                      │
│              HTML+CSS+JavaScript (Bootstrap 5)                │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask Web Server                           │
│                                                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                    Blueprints (Routes)               │    │
│  │  ┌──────────┬──────────┬──────────┬──────────────┐  │    │
│  │  │  Auth    │  Main    │  Teams   │  Matches     │  │    │
│  │  │  (login) │  (home)  │ (search) │  (fixtures)  │  │    │
│  │  └──────────┴──────────┴──────────┴──────────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                   Services (Business Logic)           │    │
│  │  ┌──────────────────┬────────────────────────────┐  │    │
│  │  │  APIFootballService           SummaryService  │  │    │
│  │  │  - get_live_matches()         - generate_match│  │    │
│  │  │  - get_standings()              _summary()     │  │    │
│  │  │  - search_teams()              - generate_team│  │    │
│  │  │  - get_match_details()          _form_summary()│  │    │
│  │  └──────────────────┴────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │               Models (SQLAlchemy ORM)               │    │
│  │  ┌──────────────────┬────────────────────────────┐  │    │
│  │  │      User        │      FavoriteTeam         │  │    │
│  │  │ - id             │ - id                       │  │    │
│  │  │ - username       │ - user_id (FK)             │  │    │
│  │  │ - email          │ - team_id                  │  │    │
│  │  │ - password_hash  │ - team_name                │  │    │
│  │  │ - favorites      │ - team_logo                │  │    │
│  │  └──────────────────┴────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────┬──────────────────────┬────────────────────┘
                  │                      │
                  ▼                      ▼
         ┌──────────────────┐   ┌──────────────────┐
         │  SQLite Database │   │  API-Football    │
         │                  │   │  (RapidAPI)      │
         │ - users          │   │                  │
         │ - favorite_teams │   │ External REST API│
         └──────────────────┘   └──────────────────┘
```

---

## 📁 Struktura adresářů

```
MatchVision/
│
├── app/                              # Hlavní aplikace
│   ├── __init__.py                   # App factory
│   ├── config.py                     # Konfigurace (3 režimy)
│   │
│   ├── models/                       # ORM modely
│   │   ├── __init__.py
│   │   └── db_models.py
│   │       ├── User (AuthMixin)
│   │       └── FavoriteTeam
│   │
│   ├── services/                     # Business logika
│   │   ├── __init__.py
│   │   ├── api_service.py            # API-Football klient
│   │   │   ├── get_live_matches()
│   │   │   ├── get_league_standings()
│   │   │   ├── get_team_details()
│   │   │   ├── get_match_details()
│   │   │   ├── search_teams()
│   │   │   └── get_team_matches()
│   │   └── summary_service.py        # Generování shrnutí
│   │       ├── generate_match_summary()
│   │       └── generate_team_form_summary()
│   │
│   ├── blueprints/                   # Flask Blueprints (routy)
│   │   ├── __init__.py
│   │   ├── auth.py                   # Autentizace
│   │   │   ├── /auth/register
│   │   │   ├── /auth/login
│   │   │   └── /auth/logout
│   │   ├── main.py                   # Hlavní stránka
│   │   │   ├── GET /
│   │   │   ├── /api/live-matches
│   │   │   ├── /leagues
│   │   │   └── /league/<id>
│   │   ├── teams.py                  # Týmy
│   │   │   ├── /teams/search
│   │   │   ├── /teams/<id>
│   │   │   ├── POST /teams/<id>/favorite
│   │   │   ├── DELETE /teams/<id>/favorite
│   │   │   └── /teams/compare
│   │   ├── matches.py                # Zápasy
│   │   │   ├── /matches/live
│   │   │   ├── /matches/<id>
│   │   │   └── /matches/<id>/summary
│   │   └── favorites.py              # Oblíbené
│   │       ├── GET /favorites/
│   │       └── GET /favorites/api
│   │
│   ├── static/                       # Statické soubory
│   │   ├── css/
│   │   │   └── style.css             # Tmavý design
│   │   │       ├── :root (barvy)
│   │   │       ├── Dark theme
│   │   │       └── Responsivní
│   │   └── js/
│   │       └── main.js               # Vanilla JS
│   │           ├── createFormChart()
│   │           ├── addTeamToFavorites()
│   │           ├── showNotification()
│   │           └── updateUI()
│   │
│   └── templates/                    # Jinja2 šablony
│       ├── base.html                 # Layout + navbar
│       ├── index.html                # Domovská stránka
│       ├── auth/
│       │   ├── register.html
│       │   └── login.html
│       ├── matches/
│       │   ├── live.html
│       │   └── detail.html
│       ├── teams/
│       │   ├── search.html
│       │   ├── detail.html
│       │   └── compare.html
│       ├── leagues.html
│       ├── league_standings.html
│       └── favorites.html
│
├── run.py                            # Entry point
├── init_db.py                        # DB inicializace
├── seed_db.py                        # Demo data
├── test_app.py                       # Testy
│
├── requirements.txt                  # Python závislosti
├── .env.example                      # Template konfigurace
├── .env                              # Skutečná konfigurace
├── .gitignore                        # Git ignore
│
├── README.md                         # Hlavní dokumentace
├── QUICKSTART.md                     # Rychlý start
├── WINDOWS_SETUP.md                  # Windows průvodce
├── DEPLOY.md                         # Deployment na Render
├── ARCHITECTURE.md                   # Toto (popis)
│
├── Dockerfile                        # Docker kontejnerizace
├── Procfile                          # Heroku/Render config
├── runtime.txt                       # Python verze
├── render.yaml                       # Render config
│
└── .github/
    └── workflows/
        └── tests.yml                 # GitHub Actions CI/CD
```

---

## 🔄 Request Flow

```
1. Uživatel otevře /
   │
   ├─→ main_bp.index()
   │   │
   │   ├─→ api_service.get_live_matches()
   │   │   └─→ requests.get(API-Football)
   │   │       └─→ returns: [match1, match2, ...]
   │   │
   │   └─→ render_template('index.html', matches=matches)
   │       └─→ base.html + index.html
   │           └─→ Uživatel vidí stránku

2. Uživatel se registruje
   │
   ├─→ auth_bp.register() [GET]
   │   └─→ render_template('auth/register.html')
   │
   └─→ auth_bp.register() [POST]
       ├─→ form.validate()
       ├─→ User.query.filter_by(username=...)
       ├─→ user.set_password(password)
       ├─→ db.session.add() + db.session.commit()
       └─→ redirect('/auth/login')

3. Uživatel přidá tým do oblíbených
   │
   └─→ teams_bp.add_favorite() [POST]
       ├─→ @login_required (Ochrana)
       ├─→ api_service.get_team_info(team_id)
       ├─→ FavoriteTeam(user_id=..., team_id=...)
       ├─→ db.session.add() + db.session.commit()
       └─→ return JSON success

4. Uživatel zobrazí detail zápasu
   │
   └─→ matches_bp.detail(match_id) [GET]
       ├─→ api_service.get_match_details(match_id)
       ├─→ summary_service.generate_match_summary(match_data)
       │   ├─→ Analýza skóre
       │   ├─→ Analýza střel
       │   └─→ Výběr szablony + formátování
       └─→ render_template('matches/detail.html', ...)
```

---

## 🗄️ Databázový model

### Tabulka: users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT uq_username UNIQUE(username),
    CONSTRAINT uq_email UNIQUE(email),
    INDEX idx_username (username),
    INDEX idx_email (email)
);
```

### Tabulka: favorite_teams
```sql
CREATE TABLE favorite_teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    team_name VARCHAR(120) NOT NULL,
    team_logo VARCHAR(500),
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT uq_user_team UNIQUE(user_id, team_id),
    INDEX idx_user_id (user_id)
);
```

---

## 🔐 Bezpečnosti

### 1. Autentizace
```python
# werkzeug.security - hashování hesel
from werkzeug.security import generate_password_hash, check_password_hash

user.set_password(password)  # PBKDF2 algoritmus
user.check_password(password)  # Bezpečné porovnání
```

### 2. Autorizace
```python
from flask_login import login_required, current_user

@teams_bp.route('/<id>/favorite', methods=['POST'])
@login_required  # Jen přihlášení uživatelé
def add_favorite(id):
    # ...
```

### 3. CSRF ochrana
```python
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    # Token se generuje automaticky
    # Ověřuje se v request bodě
```

### 4. SQL Injection ochrana
```python
# Nikdy nepoužívejte raw SQL!
# SQLAlchemy automaticky escapuje parametry

User.query.filter_by(username=username).first()
# SAFE - parametr je escapovaný

# SQLAlchemy se stará o všechny SQL injection útoky
```

### 5. XSS ochrana
```html
<!-- Jinja2 automaticky escapuje -->
{{ user.username }}  <!-- Bezpečné -->

<!-- Pokud chcete raw HTML (nebezpečné) -->
{{ user.bio | safe }}  -->  NEBEZPEČNÉ!
```

---

## 🔌 API integrace

### API-Football (RapidAPI)

**Endpoint**: `https://api-football-v1.p.rapidapi.com/v3`

**Headers**:
```
x-rapidapi-key: YOUR_KEY
x-rapidapi-host: api-football-v1.p.rapidapi.com
```

**Funkce**:
```python
api_service.get_live_matches()          # /fixtures?live=all
api_service.get_league_standings(id)    # /standings?league=X&season=2024
api_service.get_team_details(id)        # /teams/statistics?team=X
api_service.get_match_details(id)       # /fixtures?id=X
api_service.search_teams(query)         # /teams?search=X
```

**Error Handling**:
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
except requests.exceptions.RequestException as e:
    logger.error(f"API error: {e}")
    return None  # Fallback
```

---

## 📊 Diagrama User Journey

```
1. GUEST (Nepřihlášený)
   │
   ├─→ Zobrazit domovskou stránku
   ├─→ Vyhledávat týmy
   ├─→ Zobrazit detail týmu (READ-ONLY)
   ├─→ Zobrazit zápasy
   │
   ├─→ Klikne "Přidat do oblíbených"
   │   └─→ Redirect na /auth/login
   │       └─→ Přihlášení / Registrace
   │
   └─→ Stane se AUTHENTICATED USER

2. AUTHENTICATED USER
   │
   ├─→ Všechno co GUEST + více:
   │
   ├─→ Přidat tým do oblíbených (POST)
   │   └─→ FavoriteTeam se uloží v DB
   │
   ├─→ Odstranit tým z oblíbených (DELETE)
   │   └─→ FavoriteTeam se smaže z DB
   │
   ├─→ Zobrazit seznam oblíbených
   │   └─→ Query: FavoriteTeam.query.filter_by(user_id=current_user.id)
   │
   ├─→ Odhlásit se
   │   └─→ logout_user()
   │       └─→ Zpět na Guest
   │
   └─→ Přihlášení session (remember_me cookie)
```

---

## 🎨 Frontend Architecture

### CSS klasifikace

```css
:root {
    --bs-dark: #1a1a1a;        /* Tmavé pozadí */
    --bs-darker: #0d0d0d;      /* Nejčernější */
    --primary-color: #007bff;  /* Modrá */
}

/* Komponenty */
.card { }              /* Kartičky */
.btn { }               /* Tlačítka */
.alert { }             /* Upozornění */
.badge { }             /* Označení */
.table { }             /* Tabulky */

/* Responsivní */
@media (max-width: 768px) {
    .navbar-collapse { }
    .card { padding: ... }
}

/* Animace */
@keyframes fadeIn { }  /* Plynulé появlení */
@keyframes pulse { }   /* Blikání */
```

### JavaScript modularity

```javascript
// Grafy
createFormChart(canvasId, labels, data)
createStatsChart(canvasId, data)
createGoalsChart(canvasId, data)

// API calls
addTeamToFavorites(teamId)
removeTeamFromFavorites(teamId)

// UI utilities
showNotification(message, type)
formatDate(dateString)
debounce(func, wait)
```

---

## 🚀 Performance Optimizations

### 1. Caching
```python
# API-Football response cache (v budoucnu)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.cached(timeout=3600)
def get_live_matches():
    return api_service.get_live_matches()
```

### 2. Database indexing
```python
# users.py
username = db.Column(..., index=True)
email = db.Column(..., index=True)

# favorite_teams.py
user_id = db.Column(..., index=True)
```

### 3. Lazy loading
```python
# Ne všechny relace se v loadují hned
favorites = db.relationship('FavoriteTeam', lazy='select')
```

### 4. Query optimization
```python
# Avoid N+1 queries
User.query.all()  # ✅ Dobrá
User.query.filter_by(id=1).first()  # ✅ Specifický query
```

---

## 🧪 Testing Strategy

```python
# test_app.py
def test_app():
    - Kontrola importů
    - Kontrola konfigurace
    - Kontrola databáze
    - Kontrola modelů
    - Kontrola blueprintů
```

---

## 🔄 CI/CD Pipeline

```
GitHub Push
    │
    ▼
GitHub Actions (tests.yml)
    │
    ├─→ python -m flake8 app/
    ├─→ python init_db.py
    └─→ python test_app.py
        │
        ├─→ ✅ PASS
        │   └─→ Deploy povolen
        │
        └─→ ❌ FAIL
            └─→ Deploy zakázán
```

---

## 📈 Scalability (Budoucí vylepšení)

### 1. PostgreSQL místo SQLite
```
SQLite: Lokální vývoj ✅
PostgreSQL: Produkce ✅ Vít uživatelů
```

### 2. Redis Cache
```
- Cachování API odpovědí
- Session management
- Rate limiting
```

### 3. Message Queue (Celery)
```
- Asynchronní email
- Generování reportů
- Notifikace
```

### 4. Load Balancing
```
- Nginx proxy
- Multiple app instances
- Database replication
```

---

## 🎓 Konvenace

### Naming Conventions

```python
# Classes - PascalCase
class User:
    class FavoriteTeam:

# Functions/Methods - snake_case
def get_live_matches():
def add_team_to_favorites():

# Constants - UPPER_CASE
API_FOOTBALL_KEY = os.getenv(...)
CACHE_TIMEOUT = 3600

# Private - _underscore
def _make_request():

# Protected - same as public (Flask style)
def get_team_data():
```

### File Organization

```
models/db_models.py      # Datové modely
services/api_service.py  # API klientní
blueprints/auth.py       # Routy
templates/index.html     # HTML
static/css/style.css     # CSS
```

### Git Commits

```
feature: Add favorite teams functionality
fix: Correct API response parsing
docs: Update README with setup guide
test: Add user authentication tests
refactor: Simplify API service
```

---

## 📚 Další zdroje

- [Flask Best Practices](https://flask.palletsprojects.com/patterns/)
- [SQLAlchemy Guide](https://docs.sqlalchemy.org/)
- [OWASP Security](https://owasp.org/)
- [Web Dev Best Practices](https://web.dev/)

---

**Vytvořeno s ❤️ - Nadstavba pro vývoj MatchVision**
