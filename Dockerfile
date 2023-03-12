FROM python:3.10-slim-buster

RUN pip3 install pipenv
RUN apt update && apt install -y default-jre && rm -rf /var/lib/apt/lists/*

ENV PROJECT_DIR /usr/src/voliboli

WORKDIR ${PROJECT_DIR}

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system --deploy --ignore-pipfile

COPY . .

EXPOSE 80

CMD ["streamlit", "run", "Main_Page.py", "--server.port", "80"]
