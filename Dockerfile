FROM python:3.7
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 3950
COPY . /app
CMD streamlit run --server.port 3950 --server.enableCORS false spotify_artist_app.py
