## Alembic Commands

### Initialize New Alembic Environment

`alembic init`

### Create a new Revision

`alembic revision -m "<Message>"`

### Create a new Revision & Auto Generate Migration Script

`alembic revision --autogenerate -m "<MESSAGE>"`

### Updgrade to latest Revision

`alembic upgrade head`

### Upgrade to specific Revision

`alembic upgrade <Revision Number>`

### Downgrade to previous Revision

`alembic downgrade -1`

### Downgrade to N Revision

`alembic downgrade -<NUMBER>`
