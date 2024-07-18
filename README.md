# Overview

This is the API for the Community Store application, the app store for open source PWAs.

Running this project locally creates a SQLite database with users and apps tables, this MVC API provides get and post routes for them, you can also access root endpoint to view all documentation 

# Getting Started

### Requirements:

- Python installed

- A git clone of this repository

### Environment Variables:

Add an .env file to your project root. It should contain the following environment variables:

- DATABASE_NAME

- LOCALHOST

- PRODUCTION_URL

For examples, see the .env_example file

### Install the project dependencies:

```py -m pip install -r requirements.txt```

This command will install: 

- FastApi, a web framework for building APIs

- SQLModel, a library for interacting with SQL databases from Python code

- Uvicorn, an ASGI web server implementation for Python

### Running the project:

```py -m uvicorn main:app --reload```