import pika
from faker import Faker
from models import Contact
import json

def create_contacts(count=10):
    fake = Faker()
    contacts = []
    for _ in range(count):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            preferred_contact_method=fake.random_element(['email', 'sms']),
            message_sent=False
        )
        contact.save()
        contacts.append(contact)
    return contacts

def send_to_queue(contacts):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='email')
    channel.queue_declare(queue='sms')

    for contact in contacts:
        message = {'contact_id': str(contact.id)}
        if contact.preferred_contact_method == 'email':
            channel.basic_publish(exchange='', routing_key='email', body=json.dumps(message))
        else:
            channel.basic_publish(exchange='', routing_key='sms', body=json.dumps(message))
        print(f"Sent {contact.fullname} to {contact.preferred_contact_method} queue")

    connection.close()

if __name__ == "__main__":
    contacts = create_contacts(10)
    send_to_queue(contacts)
