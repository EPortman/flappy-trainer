Linting

```
poetry run flake8 .
poetry run black .
poetry run isort .
```

Run the ai trainer from the root directory

```
python -m flappy_trainer.ai.main
```

Run the game from the root directory

```
python -m flappy_trainer.main
```

Run the tests from the root directory

```
pytest -v
```

Running the Project

Dependencies
- [^python3.11](https://www.python.org/downloads/release/python-3110/)
- [pyenv](https://github.com/pyenv/pyenv)
- [poetry](https://python-poetry.org/)


Set up the Virtual Environment
```
poetry config virtualenvs.in-project true
poetry install
poetry shell
```