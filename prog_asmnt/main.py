from datetime import datetime, timedelta

class Library:
    def __init__(self):
        self.catalog = []
        self.lending_records = []

    def add_book(self, title, author, genre):
        book = {"title": title, "author": author, "genre": genre, "available": True}
        self.catalog.append(book)
        print(f"Book '{title}' added to the catalog.")

    def edit_book(self, title, new_title, new_author, new_genre):
        for book in self.catalog:
            if book["title"] == title:
                book["title"] = new_title
                book["author"] = new_author
                book["genre"] = new_genre
                print(f"Book '{title}' updated.")

    def delete_book(self, title):
        for book in self.catalog:
            if book["title"] == title:
                self.catalog.remove(book)
                print(f"Book '{title}' deleted from the catalog.")
                break

    def search_books(self, key, value, partial_match=False):
        if partial_match:
            results = [book for book in self.catalog if value.lower() in book[key].lower()]
        else:
            results = [book for book in self.catalog if book[key].lower() == value.lower()]
        return results

    def sort_books(self, key):
        self.catalog.sort(key=lambda x: x[key].lower())

    def display_books(self, books=None):
        print("Catalog:")
        if not books:
            books = self.catalog
        for book in books:
            status = "Available" if book["available"] else "Checked Out"
            print(f"{book['title']} by {book['author']} ({book['genre']}), Status: {status}")

    def display_search_results(self, key, value, partial_match=False):
        search_results = self.search_books(key, value, partial_match)
        print(f"\nSearch Results for {key} '{value}':")
        self.display_books(search_results)

    def checkout_book(self, title, user):
        for book in self.catalog:
            if book["title"] == title and book["available"]:
                book["available"] = False
                due_date = datetime.now() - timedelta(days=7) 
                self.lending_records.append((user, title, due_date))
                print(f"Book '{title}' checked out successfully. Due date: {due_date.strftime('%Y-%m-%d')}.")
                break
        else:
            print(f"Book '{title}' is not available for checkout.")

    def return_book(self, title, user):
        for book in self.catalog:
            if book["title"] == title and not book["available"]:
                book["available"] = True
                for record in self.lending_records:
                    if record[1] == title and record[0] == user:
                        self.lending_records.remove(record)
                        print(f"Book '{title}' returned successfully.")
                        break
                break
        else:
            print(f"Book '{title}' is not checked out by {user}.")

    def check_overdue_books(self):
        current_date = datetime.now()
        print("\nOverdue Books:")
        for record in self.lending_records:
            due_date = record[2]
            if due_date < current_date:
                print(f"{record[1]} (Due Date: {due_date.strftime('%Y-%m-%d')})")


# Usage:

library = Library()

# Adding books to the catalog
library.add_book("Atomic Habits", "James Clear", "Self-Help")
library.add_book("The 5 Second Rule", "Mel Robbins", "Self-Help")
library.add_book("The Lean Startup", "Eric Ries", "Business")

print("\nDISPLAYING THE CATALOG:")
# Displaying the catalog
library.display_books()

# Searching books
library.display_search_results("author", "Ja", partial_match=True)
print("SEARCH END")

# Sorting books
library.sort_books("title")
print("\nSorted Catalog START:")
library.display_books()

print("\n")

# Checking out and returning books
library.checkout_book("Atomic Habits", "User3")
library.display_books()

print("\n")

library.return_book("Atomic Habits", "User3")
library.display_books()

# Checking overdue books
library.check_overdue_books()
