# MatchVision - Deployment Guide

## Nasazení na Render.com

Render je bezplatné a jednoduché řešení pro nasazení Python webových aplikací.

### Požadavky
- GitHub účet se zvýšeným repositářem
- Render.com účet
- RapidAPI klíč pro API-Football

---

## Krok 1: Příprava GitHub repositáře

### 1.1 Inicializujte Git (pokud jste to ještě neudělali)
```bash
cd MatchVision
git init
git add .
git commit -m "Initial commit: MatchVision full-stack app"
```

### 1.2 Pushujte na GitHub
```bash
git remote add origin https://github.com/your-username/MatchVision.git
git branch -M main
git push -u origin main
```

### 1.3 Ověřte, že `.env` je v `.gitignore`
```
# Ověřte, že tento řádek je v .gitignore:
.env
```

---

## Krok 2: Vytvoření Render Web Service

### 2.1 Přejděte na Render
1. Jděte na [render.com](https://render.com)
2. Přihlaste se/Zaregistrujte se

### 2.2 Vytvoření nového Web Service
1. Klikněte "New +" v levém menu
2. Vyberte "Web Service"
3. Vyberte "Connect a repository"
4. Autorizujte GitHub přístup
5. Vyberte `MatchVision` repositář

### 2.3 Konfigurace Web Service

Vyplňte následující nastavení:

| Nastavení | Hodnota |
|-----------|---------|
| **Name** | `matchvision` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt && python init_db.py` |
| **Start Command** | `gunicorn run:app` |
| **Instance Type** | `Free` (nebo vyšší) |

### 2.4 Přidání Environment Variables

Klikněte na "Add Environment Variable" a přidejte:

```
FLASK_ENV=production
SECRET_KEY=<vygenerujte-bezpečný-klíč>
API_FOOTBALL_KEY=<váš-api-klíč-z-rapidapi>
DATABASE_URL=sqlite:///matchvision.db
```

#### Jak vygenerovat bezpečný SECRET_KEY:
```python
import secrets
print(secrets.token_hex(32))
```

#### Jak získat API_FOOTBALL_KEY:
1. Jděte na [RapidAPI - API-Football](https://rapidapi.com/api-football/api/api-football)
2. Přihlaste se
3. Klikněte "Subscribe to Test"
4. Zkopírujte váš API klíč z "X-RapidAPI-Key"

---

## Krok 3: Deploy

### 3.1 Klikněte Deploy
- Render bude automaticky:
  1. Klonovat repositář
  2. Instalovat závislosti (`requirements.txt`)
  3. Spustit `init_db.py` (vytvoří databázi)
  4. Spustit aplikaci s gunicorn

### 3.2 Čekejte na inicializaci
Zpravidla trvá 2-5 minut. Sledujte logy v "Logs" sekci.

### 3.3 Ověřte deployment
Po dokončení by měl být vidět:
```
✓ Build succeeded
✓ Your service is live
```

---

## Krok 4: Přístup k aplikaci

Vaše aplikace bude dostupná na:
```
https://matchvision-xxxxx.onrender.com
```

Render vám přidělí unikátní doménu.

---

## Ověření Deployment

### Přihlašovací údaje
Pokud jste spustili `seed_db.py`, máte demo účet:
- **Email**: demo@matchvision.com
- **Heslo**: demo123

Nebo si vytvořte nový účet přes registraci.

### Vyzkoušejte funkcionality
1. Registrase/Přihlášení
2. Vyhledávání týmu
3. Přidání do oblíbených
4. Zobrazení živých zápasů

---

## Řešení problémů

### Build selhal
Zkontrolujte "Logs" a vyhledejte chybu. Nejčastěji:
- Chybí `requirements.txt`
- Python verze není 3.8+
- Chyba v `init_db.py`

**Řešení**: Klikněte "Manual Deploy" a zkuste znovu

### Aplikace se hroutí po deployu
Zkontrolujte:
1. Jsou všechny environment variables nastaveny?
2. Je API_FOOTBALL_KEY validní?
3. Zkontrolujte logy: "Logs" tab

### Databáze není vytvořena
Render spustí `init_db.py` z Build Command. Pokud selže:
```bash
# V Render Shell:
python init_db.py
```

### "502 Bad Gateway"
1. Počkejte několik minut
2. Restartujte Web Service: "Restart Service"
3. Zkontrolujte logy

---

## Pokročilá konfigurace

### Vlastní doména
1. V Render: "Settings" → "Custom Domain"
2. Přidejte svou doménu (např. `matchvision.cz`)
3. Nakonfigurujte DNS záznamy podle instrukcí

### Databáze persistence
SQLite se v Render smaže při deployi. Pro produkci použijte:
- **PostgreSQL** (zdarma na Render)
- **MySQL** (externální)
- **MongoDB** (externální)

Měňte `DATABASE_URL` a instalujte správný driver.

### Staršíverze Python
V `runtime.txt`:
```
python-3.9.16
```

### Automatické deploye
Render automaticky deployuje při push na GitHub!

---

## Loga a Debugging

### Zobrazení logů
1. Jděte na Render Web Service
2. Klikněte "Logs" tab
3. Vidíte live logy aplikace

### Debug mode
**NEPOUŽÍVEJTE v produkci!** Debug mode není bezpečný.

```python
# run.py
if __name__ == '__main__':
    app.run(debug=False)  # Vždy False v produkci!
```

---

## Bezpečnost

### ✅ Kontrolní seznam bezpečnosti
- [ ] SECRET_KEY je dlouhý a náhodný (32+ znaků)
- [ ] API_FOOTBALL_KEY není v `requirements.txt` nebo kódu
- [ ] `.env` je v `.gitignore`
- [ ] HTTPS je povinný (Render automaticky)
- [ ] Hesla jsou hashována (Werkzeug)
- [ ] CSRF ochrana je aktivní (Flask-WTF)

### 🔒 Bezpečné SECRET_KEY
```python
import secrets
secret = secrets.token_hex(32)
print(secret)
# Vygeneruje něco jako:
# a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

---

## Monitoring a Údržba

### Sledování výkonu
- Render ukazuje CPU, RAM, Requests/sec
- Free plán má omezení: 750 hodin/měsíc
- Pokud potřebujete více, upgraďte na Starter

### Backupy databáze
SQLite není ideální pro Render. Zvažte:
1. Stahování `matchvision.db` lokálně
2. Migration na PostgreSQL
3. Pravidelné backupy

### Restartování aplikace
```bash
# V Render Dashboard:
Web Service → "Restart Service"
```

---

## Monitoring Uptime

Použijte služby jako:
- [UptimeRobot](https://uptimerobot.com) (zdarma)
- [Pingdom](https://www.pingdom.com/)
- [Healthchecks.io](https://healthchecks.io/)

---

## Upgradování na placenou verzi

Pokud aplikace prospívá, zvažte:

| Typ | Storage | RAM | Výkon |
|-----|---------|-----|-------|
| **Free** | 0.5 GB | 512 MB | Spí po 15 min |
| **Starter** | 5 GB | 512 MB | 24/7 |
| **Standard** | 20 GB | 2 GB | Produkce |

---

## Referenční zdroje

- [Render Docs](https://render.com/docs)
- [Flask Deployment](https://flask.palletsprojects.com/deployment/)
- [Gunicorn Docs](https://gunicorn.org/)
- [Python Best Practices](https://pep8.org/)

---

## Kontakt

Máte problémy s deploymentem? Zkuste:
1. Reread tohoto průvodce
2. Zkontrolujte [Render Community](https://render.com/community)
3. Otvořte issue v GitHubu

---

**Gratuluji vám k nasazení MatchVision! 🚀**

Aplikace je nyní dostupná online pro všechny.
