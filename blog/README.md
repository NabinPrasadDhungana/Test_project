# 🚀 Blog API Project

A powerful, feature-rich Blog Application backend built with **Django** and **Django Rest Framework (DRF)**. This project provides a robust API for content management, user interactions, and authentication, designed to be scalable and developer-friendly.

## ✨ Key Features

### 👤 User Management
*   **Custom User Model**: Extended user profile with Avatar support.
*   **Secure Authentication**:
    *   **JWT Authentication**: Secure, stateless authentication using `SimpleJWT`.
    *   **Session Authentication**: Traditional session-based login support.
*   **Password Validation**: Strict regex-based password policies for enhanced security.

### 📝 Content Management (Blog)
*   **Full CRUD Operations**: Create, Read, Update, and Delete blogs.
*   **Smart Categorization**: Organize blogs into categories with automatic slug generation.
*   **SEO Friendly**: Automatic slug generation for Blogs and Categories (e.g., `My Blog Post` -> `my-blog-post`).
*   **Rich Media**: Support for blog post images using `Pillow`.
*   **Author Tracking**: Automatically associates blogs with the logged-in author.

### 💬 Interactive Community
*   **Comments System**: Users can comment on blog posts.
*   **Like System**: Users can like/unlike posts (toggle functionality).
*   **Real-time counts**: Dynamic `likes_count` and `is_liked` status for the authenticated user.

### 🛠 API Capabilities
*   **RESTful Design**: Adheres to standard REST principles.
*   **Filtering & Searching**: Built-in support for searching and ordering content.
*   **Pagination**: Efficient data delivery for large datasets.

---

## 🏗 Tech Stack

*   **Language**: Python 3.x
*   **Framework**: Django 5.2.8
*   **API Framework**: Django Rest Framework 3.16.1
*   **Database**: PostgreSQL / SQLite (Configurable)
*   **Authentication**: SimpleJWT, PyJWT
*   **Utilities**: `django-environ`, `Pillow`, `django-filter`

---

## 🚀 Getting Started

Follow these steps to set up the project locally.

### Prerequisites
*   Python 3.8+
*   PostgreSQL (optional, defaults to SQLite if not configured)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root (next to `manage.py`) and add your configuration:

```env
# Database Configuration (Example for PostgreSQL)
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Security (Optional but recommended for production)
SECRET_KEY=your_secret_key
DEBUG=True
```

### 5. Run Migrations
Apply the database migrations to set up your schema.
```bash
python manage.py migrate
```

### 6. Create a Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the application running. API endpoints are generally available under `/api/`.

---

## 📚 API Documentation (Endpoints)

| Feature | Endpoint | Method(s) | Description |
| :--- | :--- | :--- | :--- |
| **Users** | `/api/users/` | `GET`, `POST` | Register or list users. |
| | `/api/users/{id}/` | `GET`, `PUT`, `DELETE` | Manage specific user details. |
| **Login** | `/api/login/` | `POST` | Session-based login (also standard JWT endpoints if configured). |
| **Categories** | `/api/categories/` | `GET`, `POST` | List or create categories. |
| **Blogs** | `/api/blogs/` | `GET`, `POST` | List all blogs or create a new one. |
| | `/api/blogs/{id}/` | `GET`, `PUT`, `DELETE` | Retrieve, update, or delete a blog. |
| **Comments** | `/api/comments/` | `GET`, `POST` | View or add comments. |
| **Likes** | `/api/likes/` | `POST` | Like a blog post. |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
