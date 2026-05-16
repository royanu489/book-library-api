# Book Library API

A REST API I built to manage a personal book library. This was my first proper backend project — I wanted to learn how APIs actually work, how to handle user login securely, and how to connect everything to a database.

Built using Python, FastAPI and SQLite.

---

## Why I built this

I kept hearing that FastAPI was one of the best frameworks to learn as a Python developer, so I decided to just build something real with it instead of only watching tutorials. A book tracker felt like a practical idea — simple enough to finish, but complex enough to cover auth, a database, and proper API structure.

---

## What it does

- Users can register and log in
- Each user gets their own book list (no one else can see or touch it)
- You can add, update, delete and search through your books
- There's a stats endpoint that gives a quick summary of your library

---

## Tech used

- **FastAPI** — the web framework
- **SQLite** — lightweight database, stored as a local file
- **SQLAlchemy** — to talk to the database using Python instead of raw SQL
- **Pydantic** — handles data validation automatically
- **JWT + Bcrypt** — for login tokens and secure password storage

---

## Project structure

```
book_api/
├── app/
│   ├── main.py         → entry point, connects everything
│   ├── database.py     → database connection setup
│   ├── models.py       → defines the User and Book tables
│   ├── schemas.py      → controls what data comes in and goes out
│   ├── auth.py         → password hashing and JWT logic
│   └── routers/
│       ├── auth.py     → register and login endpoints
│       └── books.py    → all book-related endpoints
├── requirements.txt
├── render.yaml
└── Procfile
```

---

## How to run it locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/book-library-api.git
cd book-library-api

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload
```

Then open **http://localhost:8000/docs** in your browser. You'll get an interactive page where you can test every endpoint without needing Postman.

---

## API endpoints

### Auth
| Method | Endpoint | What it does |
|--------|----------|--------------|
| POST | `/auth/register` | Create a new account |
| POST | `/auth/login` | Login and get a token |

### Books (login required)
| Method | Endpoint | What it does |
|--------|----------|--------------|
| POST | `/books/` | Add a book |
| GET | `/books/` | Get all your books |
| GET | `/books/{id}` | Get one specific book |
| PATCH | `/books/{id}` | Update a book |
| DELETE | `/books/{id}` | Delete a book |
| GET | `/books/stats/summary` | See library stats |

You can also filter and search:
- `?search=python` searches by title or author
- `?genre=Technology` filters by genre
- `?is_read=true` shows only read or unread books
- `?skip=0&limit=10` for pagination

---

## How to test it

1. Open `/docs` in your browser
2. Register a user with `POST /auth/register`
3. Login with `POST /auth/login` — copy the token from the response
4. Click the **Authorize** button at the top right and paste the token
5. Now you can use all the book endpoints

---

## Live demo

Deployed on Render: **https://book-library-api-gch1.onrender.com/docs**

> Note: The app is on a free plan so it may take 20-30 seconds to load if it hasn't been used recently. After that first load it works normally.

---

## What I learned

- How to structure a real backend project properly
- How JWT authentication works under the hood
- How ORMs like SQLAlchemy save a lot of repetitive SQL writing
- How to validate incoming data with Pydantic
- How to deploy a Python app and make it publicly accessible

---

## What I'd improve with more time

- Switch from SQLite to PostgreSQL for production use
- Add proper unit tests
- Add pagination to all list endpoints
- Add an admin role with extra permissions
