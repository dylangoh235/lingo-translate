FROM python:3.12

LABEL author="Dongyeon Go"

COPY . /lingo
WORKDIR /lingo

# .venv에 필요한 라이브러리 설치
RUN python3 -m venv .venv \
    source .venv/bin/activate \
    python3 -m pip install pip-tools \
    pip-compile -o requirements.txt pyproject.toml \
    pip-sync

# 서버 실행
ENTRYPOINT ["python", "main.py"]