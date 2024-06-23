FROM python:3.12

LABEL author="Dongyeon Goh"

COPY . /lingo
WORKDIR /lingo

# .venv에 필요한 라이브러리 설치
RUN python3 -m pip install pip-tools &&\
    pip-compile -o requirements.txt pyproject.toml &&\
    pip-sync

# 추가 패키지 설치
RUN pip install langchain_community &&\
    pip install --upgrade langchain_core langchain

# 서버 실행
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
