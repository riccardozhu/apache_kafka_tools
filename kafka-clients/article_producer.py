import os
import json
import uuid
import logging
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer
from pathlib import Path

# Configurazione del logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# Configurazione del producer
conf = {
    'bootstrap.servers': 'localhost:9092',  # Elenco dei broker Kafka
    'client.id': 'article-producer-1',
    'acks': 'all',                          # Attendi conferma da tutti i broker in-sync
    'enable.idempotence': True,             # Garantisce esattamente una consegna
    'max.in.flight.requests.per.connection': 5,  # Massimo numero di richieste in volo
    #'compression.type': 'snappy',           # Compressione dei messaggi
    #'batch.size': 32768,                    # Dimensione massima del batch in bytes
    #'linger.ms': 5,                         # Tempo di attesa massimo prima dell'invio del batch
    'security.protocol': 'PLAINTEXT',       # Protocollo di sicurezza (modifica se usi SSL/SASL)
    # 'ssl.ca.location': '/path/to/ca.pem',   # Decommentare se si usa SSL
    # 'sasl.mechanism': 'PLAIN',              # Decommentare se si usa SASL
    # 'sasl.username': 'your-username',       # Decommentare se si usa SASL
    # 'sasl.password': 'your-password',       # Decommentare se si usa SASL
    'retries': 5,                           # Numero di tentativi di reinvio in caso di errore
    'retry.backoff.ms': 100,                # Tempo di attesa tra i tentativi di reinvio
}

# Creazione del producer
producer = Producer(conf)

# Funzione di callback per la consegna dei messaggi
def delivery_report(err, msg):
    if err is not None:
        logger.error(f'Errore nella consegna del messaggio: {err}')
    else:
        logger.info(f'Messaggio consegnato con successo:')
        logger.info(f'  Topic: {msg.topic()}')
        logger.info(f'  Partizione: {msg.partition()}')
        logger.info(f'  Offset: {msg.offset()}')
        logger.info(f'  Chiave: {msg.key().decode("utf-8")}')
        logger.info(f'  Timestamp: {msg.timestamp()[1]}')

# Funzione per leggere e pubblicare i dati JSON
def publish_json_data(file_path, topic):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            
            # Assumiamo che vogliamo pubblicare l'intero contenuto come un singolo messaggio
            message = json.dumps(data)
            
            # Generazione di un UUID casuale come chiave del messaggio
            message_key = str(uuid.uuid4())
            
            logger.info(f'Pubblicazione messaggio con chiave: {message_key}')
            
            # Pubblicazione del messaggio
            producer.produce(
                topic,
                key=StringSerializer()(message_key),
                value=StringSerializer()(message),
                callback=delivery_report
            )
            
            producer.poll(0)  # Gestione degli eventi in background
    except json.JSONDecodeError:
        logger.error(f'Errore nel parsing del file JSON: {file_path}')
    except IOError:
        logger.error(f'Errore nella lettura del file: {file_path}')
    except Exception as e:
        logger.error(f'Errore imprevisto durante la pubblicazione: {str(e)}')

# Directory attuale
current_dir = Path.cwd()

# Directory contenente i file JSON
json_directory = current_dir / "flussi_articoli"  # Directory allo stesso livello dell'applicazione

# Topic Kafka
topic = 'variazioniArticoli'

# Iterazione sui file nella directory
for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(json_directory, filename)
        logger.info(f'Elaborazione del file: {filename}')
        publish_json_data(file_path, topic)

producer.flush()  # Attendere la consegna di tutti i messaggi in sospeso

logger.info("Elaborazione completata.")