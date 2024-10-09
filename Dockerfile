FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Variáveis de ambiente do MySQL
ENV MYSQL_HOST=db
ENV MYSQL_DATABASE=estacionamento
ENV MYSQL_USER=adm1
ENV MYSQL_PASSWORD=adm1
ENV AMBIENTE=PRODUCAO

CMD ["sh", "-c", "echo 'INICIANDO A APLICAÇÃO, POR FAVOR AGUARDE...' && sleep 20 && python app.py"]
