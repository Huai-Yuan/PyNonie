# NonieServer
[![CI](https://img.shields.io/github/actions/workflow/status/whyen-wang/PyNonie/ci.yml?label=CI&logo=github)](https://github.com/whyen-wang/PyNonie/actions/workflows/ci.yml)
# An app for me to learn Flask

## usage
```bash
flask --app nonie_server run --debug
flask --app nonie_server init-db  # init db
```

## test
```
coverage run -m pytest
coverage report
```

## install
```bash
pip install -e .
```

## build and install
```bash
pip install build
python -m build --wheel

pip install nonie_server-1.0.0-py3-none-any.whl
```