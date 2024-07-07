# Getting started

## Pre-requisites:

- Python installed

- A git clone of this repository

## Installing project dependendencies:

```py -m pip install -r requirements.txt```

This command gonna install: 

- FastApi, a web framework for building APIs

- SQLModel, a library for interacting with SQL databases from Python code

- Uvicorn, a ASGI web server implementation for Python

## Running the project:

```py -m uvicorn main:app --reload```

A SQLite database with a users and users habits with get and post enpoints for them gonna be created
