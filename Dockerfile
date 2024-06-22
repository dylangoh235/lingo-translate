FROM python:3.12

LABEL author="Dongyeon Goh"

COPY . /lingo
WORKDIR /lingo

# .venv에 필요한 라이브러리 설치
RUN python3 -m pip install pip-tools &&\
    pip-compile -o requirements.txt pyproject.toml &&\
    pip-sync

# 서버 실행
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]