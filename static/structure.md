recipe_book/
├── manage.py
├── recipe_book/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── recipes/
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py  # We'll add this
│   ├── views.py
│   └── templates/
│       └── recipes/
│           ├── recipe_list.html
│           ├── recipe_detail.html
│           ├── recipe_form.html
│           └── recipe_confirm_delete.html
└── staticfiles/  # For collecting static assets in production
└── media/        # For user-uploaded media (e.g., recipe images)