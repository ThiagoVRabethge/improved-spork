# Overview

API of the Community Store, a app store for free and open-source PWAS

### Tech stack:

- FastApi, a web framework for building APIs

- SQLModel, a library for interacting with SQL databases from Python code

- Uvicorn, an ASGI web server implementation for Python

# Getting Started

### Clone the project:

```bash
git clone https://github.com/ThiagoVRabethge/improved-spork
```

### Add .env file:

```bash
PG_URL=your_postgres_onrender_string_connection

LOCALHOST=http://localhost:port

PRODUCTION_URL=https://your_deployed_fast_app_url
```

### Create a virtual enviroment:

```bash
cd improved-spork
```

```bash
py -m venv [name of your environment]
```

### Install the dependencies:

```bash
py -m pip install -r requirements.txt
```

### Run the project locally:

```bash
py -m uvicorn main:app --reload
```