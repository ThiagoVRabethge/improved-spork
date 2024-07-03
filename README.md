# Getting started

pre-requisites:

- python installed

- a git clone of this repository

installing fastapi, our api routes framework:

```py -m pip install fastapi```

installing sqlmodel, our ORM:

```py -m pip install sqlmodel```

installing uvicorn, our python server:

```py -m pip install uvicorn```

finnaly, running the project:

```py -m uvicorn main:app --reload```

a database with a users table and a api with a get, get by id and post routes will be created