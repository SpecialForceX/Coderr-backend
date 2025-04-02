# Coderr Backend 💻

Dies ist das Backend für **Coderr**, eine Webplattform zur Vermittlung von IT-Dienstleistungen zwischen Freelancern und Kunden.

---

## 🔧 Tech Stack

- **Python 3.11+**
- **Django 4+**
- **Django REST Framework**
- **SQLite** (lokal) / beliebige DB für Deployment
- **Token-Auth (DRF)**
- **Modulare App-Struktur**

---

## 🚀 Lokale Entwicklung

### 1. Repo klonen

```bash
git clone https://github.com/SpecialForceX/Coderr-backend.git
cd Coderr-backend
```

### 2. Virtuelle Umgebung

```bash
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. Datenbankmigrationen

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Superuser erstellen (optional)

```bash
python manage.py createsuperuser
```

### 6. Server starten

```bash
python manage.py runserver
```

---

## 🔐 Authentifizierung

Das Projekt verwendet **Token Authentication**.

- Anmeldung per `/api/login/`
- Registrierung per `/api/registration/`
- Danach: Token in den `Authorization`-Header schicken:

```http
Authorization: Token dein_token
```

---

## 📂 Media & Static Files

- Uploads werden im Ordner `media/` gespeichert.
- Stelle sicher, dass `MEDIA_URL` und `MEDIA_ROOT` korrekt in `settings.py` gesetzt sind.

---

## 💬 Kontakt

> Entwickelt im Rahmen der Dev Akademie 👩‍💻  
