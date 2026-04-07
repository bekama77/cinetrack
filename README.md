# CineTrack

CineTrack is a Django web application for tracking movies, managing personal watchlists, writing reviews, and creating public or private movie collections.

## Live Demo
https://cinealeksandar-fkg5ete8djcacvan.spaincentral-01.azurewebsites.net/

## GitHub Repository
https://github.com/bekama77/cinetrack

---

## Overview

The platform allows users to browse movies, create personal watchlists, write reviews, and organize movies into collections.

It includes both a public
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
