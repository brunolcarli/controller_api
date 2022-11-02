run:
	python manage.py runserver 0.0.0.0:8282

migrate:
	python manage.py makemigrations
	python manage.py migrate

pipe:
	make migrate
	make run
