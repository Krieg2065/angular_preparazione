FROM joyzoursky/python-chromedriver:3.6-alpine3.7

FROM python:3
#Definisce la working directory del container
WORKDIR /app 

#Copia requirements.txt e installa le dipendenze
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#Copia tutta la cartella server
COPY . .

#Espone la porta 5000
EXPOSE 5000

#Avvia il server python
CMD [ "python", "./run.py" ]

