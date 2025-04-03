# Coderr Backend 💻

This is the backend for **Coderr**, a web platform that connects freelancers with clients for IT services.

---

# Frontend
Version 1.2.0

no changes in config.js

---

## 🔧 Tech Stack

- **Python 3.11+**
- **Django 4+**
- **Django REST Framework**
- **SQLite** (local) / Any DB for deployment
- **Token-Auth (DRF)**
- **Modulare App-Struktur**

---

## 🚀 Local Development  

### 1. Clone the repository  

```bash
git clone https://github.com/SpecialForceX/Coderr-backend.git
cd Coderr-backend
```

### 2. Create a virtual environment

```bash
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. (Optional) Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

---

## 🔐 Authentication

This project uses Token Authentication.

- Login via: `/api/login/`  
- Registration via: `/api/registration/`  
- After login, include your token in the Authorization header:  
  `Authorization: Token your_token`
```

---

## 📂 Media & Static Files

Uploads are stored in the `media/` directory.  
Make sure `MEDIA_URL` and `MEDIA_ROOT` are correctly set in your `settings.py`.

---

## 💬 Contact  
Developed as part of the Dev Akademie 👩‍💻
