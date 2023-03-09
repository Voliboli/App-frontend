FROM python:3.10-slim-buster

RUN pip3 install pipenv

ENV PROJECT_DIR /usr/src/voliboli_api

WORKDIR ${PROJECT_DIR}

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --deploy --ignore-pipfile

COPY . .

EXPOSE 8501

CMD ["pipenv", "run", "streamlit", "run", "app.py"]