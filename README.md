# springhackathon22


## Setup 
```
python3
from bahay import *
db.create_all()
flask db init
```

## Run after changes to db
```
flask db migrate -m "initial migration"
flask db upgrade
```


## Run after installing
```
pip freeze > requirements.txt
```

## Run Application
```
. venv/bin/activate
export FLASK_APP=hello
export FLASK_ENV=development
flask run
```