import pika
import json
from models import Contact

def send_sms(contact):
    # Імітація надсилання SMS
    print(f"Sending SMS to {contact.phone_number}")
    contact.message_sent = True
    contact.save()
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

def send_sms(contact_id):
    print(f"Sending SMS to contact {contact_id}")

    contact = Contact.objects(id=contact_id).first()
    if contact:
        contact.message_sent = True
        contact.save()
        print(f"SMS sent to {contact.fullname}")

def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    send_sms(contact_id)
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='sms')

channel.basic_consume(queue='sms', on_message_callback=callback)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

def callback(ch, method, properties, body):
    data = json.loads(body)
    contact = Contact.objects(id=data['contact_id']).first()
    if contact:
        send_sms(contact)
    ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='sms_queue')
    channel.basic_consume(queue='sms_queue', on_message_callback=callback)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
