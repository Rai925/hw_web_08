import pika
import json
from models import Contact
from mongoengine import connect
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'USER')
mongodb_pass = config.get('DB', 'PASS')
db_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')

connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)

def send_email(contact_id):
    print(f"Sending email to contact {contact_id}")

    contact = Contact.objects(id=contact_id).first()
    if contact:
        contact.message_sent = True
        contact.save()
        print(f"Email sent to {contact.fullname}")

def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    send_email(contact_id)
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email')

channel.basic_consume(queue='email', on_message_callback=callback)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
