# music zone back end

using django django-rest-framework.

# Run

1. make a virtual environment.
2. install the required packages.

```python
pip install -r requirements
```

3. database migrate

```python
python manage.py makemigrations content
python manage.py migrate
```

4. start the project

```python
python manage.py runserver
```

5. load test data

- make sure the folder named `test_data` exists.
- run `python manage.py test` to load test data.
- http://127.0.0.1:8000/clear/ is for clear all data associated with music
