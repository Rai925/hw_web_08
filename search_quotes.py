from models import Author, Quote

def find_quotes_by_author(name):
    authors = Author.objects(fullname__icontains=name)
    quotes = Quote.objects(author__in=authors)
    for quote in quotes:
        print(quote.quote)

def find_quotes_by_tag(tag):
    quotes = Quote.objects(tags__icontains=tag)
    for quote in quotes:
        print(quote.quote)

def find_quotes_by_tags(tags):
    tags_list = tags.split(',')
    quotes = Quote.objects(tags__in=tags_list)
    for quote in quotes:
        print(quote.quote)

def main():
    while True:
        command = input("Enter command (name:author, tag:tag, tags:tag1,tag2, exit): ")
        if command.startswith('name:'):
            name = command[5:]
            find_quotes_by_author(name)
        elif command.startswith('tag:'):
            tag = command[4:]
            find_quotes_by_tag(tag)
        elif command.startswith('tags:'):
            tags = command[5:]
            find_quotes_by_tags(tags)
        elif command == 'exit':
            break
        else:
            print("Unknown command")

if __name__ == '__main__':
    main()
