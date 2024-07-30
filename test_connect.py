from connect import connect_to_db
from models import Author

def test_connection():
    connect_to_db()
    try:
        test_author = Author(fullname="Test Author", born_date="2024-01-01", born_location="Test Location", description="Test Description")
        test_author.save()
        print("Підключення до бази даних успішне.")
        test_author.delete()
    except Exception as e:
        print(f"Помилка підключення до бази даних: {e}")

if __name__ == "__main__":
    test_connection()
