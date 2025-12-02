# Kitob do'koni (Django 5)

## O'rnatish
1. Python 3.12 o'rnating.
2. Virtual muhit: `python -m venv .venv && source .venv/bin/activate` (Windows: `.venv\\Scripts\\activate`).
3. Kutubxonalar: `pip install -r requirements.txt`.
4. Migratsiyalar: `python manage.py migrate`.
5. Admin yaratish: `python manage.py createsuperuser`.
6. Statik/mediaga papkalar: `backend/static/`, `backend/media/` mavjud.
7. Server: `python manage.py runserver`.

## Foydali URL lar
- Bosh sahifa: `/`
- Kategoriya: `/kategoriya/<slug>/`
- Kitob: `/kitob/<id>/<slug>/`
- Qidiruv: `/qidiruv/?q=...`
- Savat: `/savat/`
- Buyurtma: `/buyurtma/`
- Admin: `/admin/`
