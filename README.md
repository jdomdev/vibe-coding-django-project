# 📚 Recipe Book Application 🍽️

> **A project developed in the field of *vibe-coding* and *prompt engineering***  
> Prompt engineering techniques such as *simple prompts*, *Retrieval-Augmented Generation (RAG)*, and *fine-tuning* are explored and prototyped in parallel through this interface.

- **Vibe-coding** is a relaxed, creative style of coding where aesthetics, exploration, and learning guide development — not just specifications.
- **Simple prompts** involve direct natural language queries (e.g., « List all recipes with pasta ») without additional context or memory.
- **RAG (Retrieval-Augmented Generation)** integrates external information (e.g., recipe embeddings or vector search) into prompt responses for enhanced output.
- **Fine-tuning** refers to adapting pre-trained language models to better fit domain-specific needs — such as culinary vocabulary, formatting, or user interactions in recipe databases.

---

## ✨ Features

- **Recipe Listing** 📖 – View all stored recipes with their image, title, and a short description.
- **Add New Recipe** ➕ – Add recipes by providing a title, uploading an image or linking to a URL, listing ingredients, and steps.
- **View Recipe Details** 🔍 – See full details of any recipe.
- **Edit Recipe** ✍️ – Modify the details of any recipe.
- **Delete Recipe** 🗑️ – Remove recipes from your collection.

---

## 🛠️ Requirements and Dependencies

Ensure you have the following installed:

- `Python` 🐍 – Version 3.9 or higher is recommended.
- `uv` – A blazing-fast Python package installer and dependency manager.

Install `uv` (if you don't have it):

```bash
pip install uv
````

Main Python dependencies:

```bash
uv pip install Django Pillow
```

* `Django` 🚀 – The powerful web framework.
* `Pillow` 🖼️ – Required for handling image uploads.

---

## 🚀 Installation Instructions

Clone the repository:

```bash
git clone https://github.com/your-username/recipe-book.git
cd recipe-book
```

> Replace the URL above with your actual repository.

---

### Create and Activate a Virtual Environment

Using `uv`:

```bash
uv venv
```

Activate it:

* **macOS/Linux** 🖥️:

  ```bash
  source .venv/bin/activate
  ```

* **Windows** 🪟:

  ```bash
  .venv\Scripts\activate
  ```

Install dependencies:

```bash
uv pip install Django Pillow
```

---

## 🗄️ Database Setup

Create and apply migrations:

```bash
python manage.py makemigrations recipes
python manage.py migrate
```

---

### (Optional) Create a Superuser

Access Django Admin by creating a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to set your username, email, and password.

---

## 🖥️ Run the Server

Start Django development server:

```bash
python manage.py runserver
```

Visit:

* **Recipe List** → `http://127.0.0.1:8000/recipes/`
* **Admin Panel** → `http://127.0.0.1:8000/admin/`

---

## 🧪 Running Tests

Run tests for the `recipes` app:

```bash
python manage.py test recipes
```

This runs all unit and integration tests located in `recipes/tests.py`.

---

## 📂 Project Structure

```
recipe_book/
├── manage.py
├── recipe_book/            # ⚙️ Main project configuration
│   ├── settings.py         # Global settings
│   ├── urls.py             # URL routing
│   └── ...
├── recipes/                # 🍳 Core recipe application
│   ├── migrations/         # Database schema history
│   ├── templates/recipes/  # 📄 HTML templates
│   ├── admin.py            # Django Admin config
│   ├── apps.py             # App setup
│   ├── forms.py            # 📝 Forms for recipe creation/editing
│   ├── models.py           # 📖 Recipe model
│   ├── tests.py            # ✅ Unit tests
│   ├── urls.py             # App-specific routes
│   └── views.py            # 👁️ Class-Based Views
├── static/                 # 🌐 Static files (CSS, JS, etc.)
├── media/                  # 📸 User-uploaded images
└── .venv/                  # 📦 Virtual environment
```

---

## 👋 Contributing

Contributions are welcome! Feel free to fork the repo, make changes, and submit a pull request.

Let’s improve this Recipe Book together 💖

---

## ⚖️ License

This project is licensed under the **MIT License**.
See `LICENSE.md` for full details.

```

---

Would you like a 🇫🇷 French version too? Or want me to include badges, screenshots, or an advanced Prompt Engineering section with examples?
```
