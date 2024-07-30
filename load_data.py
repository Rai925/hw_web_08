import json
from models import Author, Quote

def load_authors(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        authors = json.load(file)
        for author in authors:
            new_author = Author(
                fullname=author['fullname'],
                born_date=author['born_date'],
                born_location=author['born_location'],
                description=author['description']
            )
            new_author.save()

def load_quotes(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        quotes = json.load(file)
        for quote in quotes:
            author = Author.objects(fullname=quote['author']).first()
            if author:
                new_quote = Quote(
                    tags=quote['tags'],
                    author=author,
                    quote=quote['quote']
                )
                new_quote.save()

if __name__ == '__main__':
    load_authors('authors.json')
    load_quotes('quotes.json')
