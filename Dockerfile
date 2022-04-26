FROM python:3.10.4-slim
LABEL maintainer="Konstantinos K @KonScanner"

EXPOSE 8501:80

WORKDIR /app
COPY requirements.txt .
COPY scripts/setup.sh .
COPY config.json .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app /app
CMD sh setup.sh && streamlit run main.py
