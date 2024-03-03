# Course Async Architecture

#### Here will be homework from this course


## How to start development

1. Create virtual environment:

```bash
python -m venv venv
````

2. Activate virtual environment in your IDE or using command:

```bash
venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.dev.txt
```

4. Install pre-commit hooks:
```bash
pre-commit install
```
5. Fill env variables by [example](.env.example) in .env file
6. Run project with dev-settings:
```bash
docker compose -f docker-compose.yml -f docker-compsoe.dev.yml up
```
