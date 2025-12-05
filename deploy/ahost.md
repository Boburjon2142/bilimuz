## aHost deploy bo‘yicha tezkor qo‘llanma (SQLite default)

### 1. Muhitni tayyorlash
- Python 3.12 o‘rnatilgan bo‘lishi kerak.
- Kodni serverga joylashtiring (git clone yoki zip orqali).
- Virtual muhit: `python -m venv .venv && source .venv/bin/activate` (Windows: `.venv\Scripts\activate`).
- Kutubxonalar: `pip install -r requirements.txt`

### 2. Muhit o‘zgaruvchilari (.env)
Serverda `.env` yarating (SQLite uchun soddalashtirilgan):
```
DJANGO_SECRET_KEY=super-secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=bilimstore.uz,www.bilimstore.uz
DJANGO_CSRF_TRUSTED_ORIGINS=https://bilimstore.uz,https://www.bilimstore.uz
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_DB_ENGINE=sqlite
```
> Postgres kerak bo‘lsa `DJANGO_DB_ENGINE=postgres` qiling va POSTGRES_* maydonlarini qo‘shing.

### 3. Ma’lumotlar bazasi
- SQLite: `python manage.py migrate` (agar `db.sqlite3` tayyor bo‘lsa uni ham yuklab qo‘yish mumkin).
- Postgres (ixtiyoriy): aHost panelida DB yarating, `.env` ni Postgres ma’lumotlari bilan to‘ldiring, keyin `python manage.py migrate`.

### 4. Statik va media
- Statiklarni yig‘ish: `python manage.py collectstatic --noinput`
- `STATIC_ROOT`: `staticfiles/` (settings.py da mavjud). Apache/Nginx orqali `staticfiles/` ni serv qiling.
- Media uchun `backend/media/` katalogini web-serverdan servis qiling (yoki S3/MinIO).

### 5. Gunicorn (WSGI)
- Lokal test: `gunicorn backend.backend.wsgi:application --bind 0.0.0.0:8000`
- Systemd unit (misol):
```
[Unit]
Description=Gunicorn for bookstore
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/bookstore
EnvironmentFile=/path/to/bookstore/.env
ExecStart=/path/to/bookstore/.venv/bin/gunicorn backend.backend.wsgi:application --bind unix:/path/to/bookstore/gunicorn.sock --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

### 6. Reverse proxy (Nginx)
```
server {
    listen 80;
    server_name bilimstore.uz www.bilimstore.uz;

    location /static/ {
        alias /path/to/bookstore/staticfiles/;
    }
    location /media/ {
        alias /path/to/bookstore/backend/media/;
    }
    location / {
        proxy_pass http://unix:/path/to/bookstore/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 7. Xavfsizlik
- `DJANGO_DEBUG=False` ni ta’minlang.
- HTTPS orqasida ishlaganda `DJANGO_SECURE_SSL_REDIRECT=True`, cookie secure flaglari env orqali yoqiladi.
- Admin uchun kuchli parol va (imkon bo‘lsa) IP cheklash.

### 8. Tekshirish
- `python manage.py check`
- `gunicorn ...` bilan qo‘lda ko‘rib chiqing, keyin systemd ni ishga tushiring: `sudo systemctl enable --now gunicorn`
- Nginx reload: `sudo nginx -s reload`
