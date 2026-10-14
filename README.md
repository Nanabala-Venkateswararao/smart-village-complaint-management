# Smart Village Complaint Management System

A beginner-friendly Django project using SQLite.

## Features
- Villager registration/login/logout
- Submit complaints with category, village/location, description, optional image
- Users can see their own complaints and status
- Staff/admin can view all complaints and update status
- Search/filter complaints
- Django admin

## Setup (Windows)

1. Install Python 3.11+ and open Command Prompt in this folder.
2. Create and activate a virtual environment:

   ```bat
   python -m venv env
   env\Scripts\activate
   ```

3. Install dependencies:

   ```bat
   python -m pip install -r requirements.txt
   ```

4. Create database tables:

   ```bat
   python manage.py makemigrations complaints
   python manage.py migrate
   ```

5. Create an administrator:

   ```bat
   python manage.py createsuperuser
   ```

6. Start the server:

   ```bat
   python manage.py runserver
   ```

7. Open http://127.0.0.1:8000/ in your browser.
   Admin: http://127.0.0.1:8000/admin/

## Official account
Create a superuser, sign in at `/admin/`, and use Django's admin interface. To use the official dashboard at `/official/`, mark an account as Staff in Django admin (Users).

## Important notes
- This is a learning/demo project. Before real deployment, configure `DEBUG=False`, a strong secret key, allowed hosts, HTTPS, backups, and proper privacy/security controls.
- Never commit passwords or your real production secret key.
- Uploaded complaint images are stored in `media/`.
