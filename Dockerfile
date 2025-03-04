FROM python:3.12-slim-bookworm

WORKDIR /cypher

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "main.py"]
