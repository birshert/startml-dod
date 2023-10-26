FROM python:3.10-slim

WORKDIR /app

RUN pip install streamlit --no-cache-dir

COPY . .

EXPOSE 55556

CMD streamlit run main.py --server.port 55556