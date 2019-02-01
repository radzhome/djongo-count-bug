## Djongo count bug reproduction



### Manual setup

Requires python3

1. install docker - https://docs.docker.com/install/

1. Bring up mongo
```sh
docker-compose up -d mongo
# or
docker-compose run -d mongo
```

1. python3 manage.py migrate

1. create a super user
```bash
python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')"
```

1. python3 manage.py generate_content -n 2500000

1. python3 manage.py runserver

1. Go to http://127.0.0.1:8000/admin/ and login admin:admin


## Misc

* Reset network - `docker network prune`
