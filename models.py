from mongoengine import Document, StringField, EmailField, BooleanField, ListField, ReferenceField
from connect import connect_to_db

connect_to_db()

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()

class Contact(Document):
    fullname = StringField(required=True)
    email = EmailField(required=True, unique=True)
    phone = StringField(required=True, unique=True)
    preferred_contact_method = StringField(choices=['email', 'sms'])
    message_sent = BooleanField(default=False)
