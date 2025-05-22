<a id="top"></a>

<h1 align="center">BASIC BACKEND API EXAMPLE FOR LAB MANAGEMENT</h1>

<p>This application manages three main aspects: <strong>users, clients, and samples</strong>. It also includes a <strong>history feature</strong> to store logs of platform changes, such as creations, updates, and deletions. Additionally, it supports <strong>role-based access control</strong> and <strong>refresh token authentication</strong>.</p>

---

## 🛠️ Built With

This application was developed using Python 3.11.4 and the following main libraries:

- FastAPI
- PostgreSQL
- Redis
- PyJWT
- dotenv

<p align="right">(<a href="#top">back to top</a>)</p>

---

## 🚀 Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/github_username/repo_name.git
   cd repo_name

2. Create a .env file in the root directory with the following structure:
    ```bash
    DATABASE_URL=
    JWT_SECRET_KEY=
    JWT_ALGORITHM=
    REDIS_HOST=
    REDIS_PORT=
3. Run the application with FastAPI:
```bash
   fastapi dev app/