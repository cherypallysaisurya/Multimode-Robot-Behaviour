# Contributing

## Dev Install
```
pip install -e .[hardware,visual]
```

## Run Tests
```
pytest -q
```

## Build
```
python -m build
```
This creates `dist/myrobot-<version>.tar.gz` and `.whl`.

## Publish (PyPI)
```
pip install twine
python -m twine upload dist/*
```

## Versioning
Update `project.version` in `pyproject.toml` before build.
