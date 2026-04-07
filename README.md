# CineTrack

CineTrack is a Django web application for tracking movies, managing personal watchlists, writing reviews, and building public or private collections.

It includes:
- custom user model and profile
- public movie catalog and review pages
- private watchlist, dashboard, recommendations, and collections
- DRF API endpoints
- Celery background task for weekly recommendations
- demo data and groups setup commands
- automated tests
- deployment-ready settings for Render

## Tech stack

- Python 3.11+
- Django 5+
- Django REST Framework
- SQLite by default for easy local startup
- PostgreSQL supported through environment variables
- Celery + Redis
- Bootstrap 5
- Gunicorn + WhiteNoise for deployment

## Quick start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a `.env` file

Copy `.env.example` to `.env`.

By default the project uses SQLite, so you can start immediately without creating a database server.

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Create groups and demo data

```bash
python manage.py setup_groups
python manage.py seed_demo_data
```

The demo command creates a starter user:
- username: `demo_user`
- password: `demo12345`

### 5. Run the server

```bash
python manage.py runserver
```

## Optional PostgreSQL setup

If you want PostgreSQL locally, set this in `.env`:

```env
DB_ENGINE=postgres
DB_NAME=cinetrack_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
```

Then create the database and run migrations again.

## Useful commands

```bash
python manage.py createsuperuser
python manage.py test
python manage.py setup_groups
python manage.py seed_demo_data
```

## Celery

Start a worker with:

```bash
celery -A cinetrack worker -l info
```

The project ships with a weekly recommendation task in `watchlists/tasks.py`.

## API endpoints

- `/api/movies/`
- `/api/movies/<slug>/`
- `/api/reviews/`
- `/api/watchlist/`
- `/api/watchlist/<id>/`

## Deployment on Render

### Files included

- `build.sh`
- `render.yaml`
- env-based `settings.py`
- `gunicorn`, `whitenoise`, and `dj-database-url` in `requirements.txt`

### Manual deploy steps

1. Push the project to GitHub.
2. In Render, create a PostgreSQL database.
3. Create a new Web Service connected to your GitHub repo.
4. Set these values:

**Build Command**

```bash
./build.sh
```

**Start Command**

```bash
gunicorn cinetrack.wsgi:application
```

### Required environment variables

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-service-name.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-service-name.onrender.com
DATABASE_URL=<Render PostgreSQL connection string>
```

If you plan to use Celery in production, also configure:

```env
CELERY_BROKER_URL=redis://...
CELERY_RESULT_BACKEND=redis://...
```

### Notes

- `DATABASE_URL` takes priority over the local SQLite/PostgreSQL fallback settings.
- `build.sh` runs `collectstatic`, migrations, groups setup, and demo data seeding.
- WhiteNoise is enabled for static files.

## Default groups

- `Curators` — movie and genre management permissions
- `Moderators` — review moderation permissions

Create them with:

```bash
python manage.py setup_groups
```

## Next improvements

- add Celery Beat scheduling
- add public user profiles
- add better filtering by year / rating / genre
- add cloud media storage
- tighten production security further
