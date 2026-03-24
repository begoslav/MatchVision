# MatchVision - Windows Setup Guide

Kompletní průvodce pro instalaci a spuštění aplikace na Windows.

## ✅ Předpoklady

- Windows 10/11
- Python 3.8+ nainstalovaný ([stáhněte zde](https://www.python.org/downloads/windows/))
- Git (volitelné, ale doporučené)
- Editor kódu (VS Code, PyCharm apod., volitelné)

---

## Krok 1: Ověřte instalaci Python (DŮLEŽITÉ!)

Otevřete **Command Prompt** (Win+R → `cmd` → Enter)

```cmd
python --version
```

Mělo by vrátit něco jako:
```
Python 3.9.13
```

❌ Pokud je chyba "python: command not found":
1. Přejděte na https://www.python.org/downloads/
2. Stáhněte nejnovější Python 3.11+
3. **DŮLEŽITÉ**: Při instalaci zaškrtněte "Add Python to PATH"
4. Restartujte Command Prompt

---

## Krok 2: Navigace na projekt

Otevřete **Command Prompt** a přejděte do složky projektu:

```cmd
cd C:\Users\georg\OneDrive\Plocha\TP\MatchVision
```

Ověřte, že jste ve správné složce:
```cmd
dir
```

Měli byste vidět:
```
app/  requirements.txt  run.py  .env  README.md
```

---

## Krok 3: Vytvoření virtuálního prostředí

Vytvořte virtuální prostředí (izolovanou Python instalaci):

```cmd
python -m venv venv
```

Trvá to cca 1-2 minuty...

---

## Krok 4: Aktivace virtuálního prostředí

**To je NEJDŮLEŽITĚJŠÍ! Musíte to dělat vždy, když otevřete Command Prompt.**

```cmd
venv\Scripts\activate
```

Vidět budete na začátku řádky: `(venv)`

Příklad:
```cmd
(venv) C:\Users\georg\OneDrive\Plocha\TP\MatchVision>
```

❌ Pokud nevidíte `(venv)`:
- Uzavřete Command Prompt
- Otevřete znovu
- Navigujte do MatchVision složky
- Znovu spusťte `venv\Scripts\activate`

---

## Krok 5: Instalace závislostí

S aktivovaným virtuálním prostředím (vidíte `(venv)`):

```cmd
pip install -r requirements.txt
```

Instalace trvá 2-5 minut. Čekejte na:
```
Successfully installed Flask-3.0.0 Flask-SQLAlchemy-3.1.1 ...
```

---

## Krok 6: Konfigurace API klíče

Editujte soubor `.env` (můžete ho otevřít v Notepadu):

```cmd
notepad .env
```

Přidejte váš API klíč z RapidAPI:

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-12345
DATABASE_URL=sqlite:///matchvision.db
API_FOOTBALL_KEY=váš_api_klíč_z_rapidapi
```

Uložte (Ctrl+S) a zavřete editor.

### Jak získat API_FOOTBALL_KEY:

1. Jděte na https://rapidapi.com/api-football/api/api-football
2. Klikněte "Subscribe to Test" (zdarma)
3. Přejděte na "Code Snippets"
4. Zkopírujte hodnotu "x-rapidapi-key"
5. Vložte ji do `.env` namísto `váš_api_klíč_z_rapidapi`

---

## Krok 7: Inicializace databáze

```cmd
python init_db.py
```

Měli byste vidět:
```
Vytvářím databázi...
✅ Databáze vytvořena úspěšně!

Vytvořené tabulky: 2
  - users
  - favorite_teams
```

---

## Krok 8: (Volitelné) Vytvoření demo uživatele

```cmd
python seed_db.py
```

Vytvoří demo účet:
- **Username**: demo
- **Heslo**: demo123

---

## Krok 9: Spuštění aplikace

```cmd
python run.py
```

Měli byste vidět:
```
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

---

## Krok 10: Otevření aplikace

Otevřete prohlížeč a jděte na:
```
http://localhost:5000
```

Vidět byste měli domovskou stránku MatchVision! 🎉

---

## Zastavení aplikace

V Command Prompt, kde běží aplikace:
```cmd
CTRL+C
```

---

## Příští spuštění (zkrácená verze)

Příště stačí v Command Prompt:

```cmd
cd C:\Users\georg\OneDrive\Plocha\TP\MatchVision
venv\Scripts\activate
python run.py
```

A otevřete http://localhost:5000

---

## 🔥 Běžné chyby na Windows

### ❌ "python: command not found"
```cmd
Řešení: Přeinstalujte Python a zaškrtněte "Add Python to PATH"
```

### ❌ "venv\Scripts\activate je zakázaný"
```cmd
Řešení: Spusťte Command Prompt jako Administrator (Win+X → CMD - Admin)
```

### ❌ "ModuleNotFoundError: No module named 'flask'"
```cmd
Problém: Zapomínáte aktivovat virtuální prostředí!
Řešení: Spusťte: venv\Scripts\activate
Měli byste vidět (venv) na začátku řádky
```

### ❌ "Port 5000 is already in use"
```cmd
Problém: Něco jiného používá port 5000
Řešení: Zavřete ostatní aplikace nebo přejděte na jiný port:
python run.py --port 5001
```

### ❌ "API not configured"
```cmd
Problém: API klíč není v .env
Řešení: Otevřete .env a vložte svůj API klíč
notepad .env
Uložte (Ctrl+S)
Restartujte aplikaci
```

### ❌ "database is locked"
```cmd
Problém: Databáze je uzamčená
Řešení: Smažte matchvision.db a vytvořte znovu
del matchvision.db
python init_db.py
```

---

## 📁 Používání souborů

### Editace kódu
Otevřete složku v editoru:
```cmd
code .
```
(Pokud máte VS Code nainstalovaný)

### Přidání souboru
1. Pravý klik v Exploreru → Nový soubor
2. Přejmenujte na `název.py`
3. Editujte v editoru

### Smazání souboru
1. Pravý klik
2. Delete (nebo Shift+Delete pro trvalé smazání)

---

## 🌐 Nasazení na Render

Jakmile má vše běžet lokálně:

1. Pushujte kód na GitHub:
```cmd
git add .
git commit -m "MatchVision app ready"
git push
```

2. Jděte na https://render.com
3. Vyberte GitHub repositář
4. Nastavte Build Command na: `pip install -r requirements.txt && python init_db.py`
5. Start Command: `gunicorn run:app`
6. Deploy!

Viz `DEPLOY.md` pro detaily.

---

## 📚 Další prostředky

- [Python na Windows](https://docs.python.org/3/using/windows.html)
- [Virtual Environments](https://docs.python.org/3/library/venv.html)
- [Flask Tutorial](https://flask.palletsprojects.com/tutorial/)

---

## 💡 Tipy pro Windows

### Snadnější navigace
```cmd
# Zkrácení cesty
subst M: "C:\Users\georg\OneDrive\Plocha\TP\MatchVision"
cd M:
```

### PowerShell místo Command Prompt
PowerShell je modernější:
```powershell
winget install Python.Python.3.11  # Instalace Pythonu (win 11)
```

### VS Code Terminal
```
Ctrl+` (backtick) - Otevřít Terminal v VS Code
```

Automaticky aktivuje virtuální prostředí!

---

## ✨ Pokročilé tipsy

### Requirements.txt generování
Pokud chcete sdílet projekt:
```cmd
pip freeze > requirements.txt
```

### Poetry (alternativa k venv)
```cmd
pip install poetry
poetry init
poetry install
```

### Spuštění bez otevírání Command Prompt
Vytvořte `start.bat`:
```batch
@echo off
cd /d "%~dp0"
venv\Scripts\activate
python run.py
```

Dvakrát klikněte na `start.bat` pro spuštění!

---

## 🎓 Naučte se Python

Doporučené kurzy:
- [Real Python Tutorials](https://realpython.com/)
- [Codecademy Python Course](https://www.codecademy.com/learn/learn-python)
- [Udemy Python for Everybody](https://www.udemy.com/course/python-for-everybody/)

---

## 🆘 Pokud nic nefunguje

1. Zkrokem tento průvodce znovu pečlivě
2. Zkontrolujte všechny výzvy výš
3. Čtěte chybové zprávy - jsou velmi informativní!
4. Zkuste Google + vaše chybová zpráva

---

Máte otázky? Podívejte se na README.md nebo QUICKSTART.md.

**Vítejte v MatchVision! ⚽**
