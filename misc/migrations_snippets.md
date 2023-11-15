## Migrations:

#### Manually run migrations (optional: migrations would run on first app start. See app/__init__.py):
`flask db upgrade`

#### Re-create migrations from scratch if needed:
- Delete ./migrations
- flask db init
- Generate migration file (see below)
- flask db upgrade

Version file template:
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

#### Autogenerate migrations for schema changes:
`flask db migrate -m "Initial migration"`

#### Generate empty migration:
`flask db revision -m "Save locations to db"`


## Some links:
https://realpython.com/flask-by-example-part-1-project-setup/

https://towardsdatascience.com/deploy-a-micro-flask-application-into-heroku-with-postgresql-database-d95fd0c19408

https://flatlogic.com/blog/top-mapping-and-maps-api/

