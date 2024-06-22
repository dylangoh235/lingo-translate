# How to setup

1. python3 -m venv .venv
2. source .venv/bin/activate
3. python3 -m pip install pip-tools
4. pip-compile -o requirements.txt pyproject.toml
5. pip-sync
