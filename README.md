# Django Blog with User Authentication

A full-featured blog application built with Django, featuring user authentication, post management, and draft mode functionality.

## Features

**User Authentication**
- Sign up, login, and logout functionality
- Conditional navigation based on authentication status
- Posts automatically assigned to logged-in user

**Post Management**
- Create, read, update, and delete blog posts
- Only post authors can edit or delete their own posts
- Image upload support

**Draft Mode**
- Posts can be created with different status modes (Draft, Published, Archived)
- Users can change post status by editing the post
- Draft posts are saved but not yet published

**Design**
- Custom purple gradient theme with glassmorphic UI elements
- Responsive design

## Technologies Used

- Django 5.2.8
- Python 3.14
- SQLite
- HTML5/CSS3
- Bootstrap 5
- django-crispy-forms
- Pillow

## Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd blog
```

2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser
```bash
python manage.py createsuperuser
```

6. Create Status records in admin
- Run server: `python manage.py runserver`
- Go to http://127.0.0.1:8000/admin
- Create three Status objects:
  - Published: "Posts available for all to view"
  - Draft: "Posts visible only to the author"
  - Archived: "Old posts visible only to logged-in users"

7. Access the application at http://127.0.0.1:8000/

## Usage

**Creating Posts**
1. Log in to your account
2. Click "Create Post" in the navbar
3. Fill in title, subtitle, body, and optionally upload an image
4. Select status (Draft, Published, or Archived)
5. Click "Create Post"

**Publishing Drafts**
1. Navigate to your draft post
2. Click "Edit Post"
3. Change status from "Draft" to "Published"
4. Click "Save Changes"

## Database Models

**Post Model**
- Title, Subtitle, Body
- Author (ForeignKey to User)
- Status (ForeignKey to Status)
- Image (optional)
- Created_on timestamp

**Status Model**
- Name (unique)
- Description

**Comment Model**
- Post (ForeignKey to Post)
- Author (ForeignKey to User)
- Body
- Created_on timestamp

## Course Information

Full-Stack Development Bootcamp
San Diego Global Knowledge University
Unit 113 - Intermediate Django

## Author

Micah Weathers
- GitHub: github.com/micahweathers
- Email: mweathers.dev@gmail.com