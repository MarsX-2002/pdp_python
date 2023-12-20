# Library Management System

This Python application serves as a simple Library Management System, allowing users to manage a small library or book collection. The system includes functionalities for adding, editing, and deleting book entries, searching and sorting books, checking out and returning books, and keeping track of lending records. Additionally, it provides a summary of the library's status and can identify overdue books.

## Class Overview

### Library Class

The `Library` class is the core component of the system, encapsulating the functionality for managing the library.

#### Methods:

1. **`add_book(title, author, genre):`**
   - Adds a new book to the library catalog.

2. **`edit_book(title, new_title, new_author, new_genre):`**
   - Edits the information of an existing book in the catalog.

3. **`delete_book(title):`**
   - Deletes a book from the catalog.

4. **`search_books(key, value, partial_match=False):`**
   - Searches for books based on the specified key and value.
   - Supports partial matching if `partial_match` is set to `True`.

5. **`sort_books(key):`**
   - Sorts the library catalog based on the specified key.

6. **`display_books(books=None):`**
   - Displays the entire catalog or a specified list of books.

7. **`display_search_results(key, value, partial_match=False):`**
   - Displays the search results based on the specified key and value.
   - Supports partial matching if `partial_match` is set to `True`.

8. **`checkout_book(title, user):`**
   - Checks out a book to a user, updating its availability and adding a lending record with a due date.

9. **`return_book(title, user):`**
   - Returns a checked-out book, updating its availability and removing the lending record.

10. **`check_overdue_books():`**
    - Checks and displays overdue books based on the lending records.

### Example Usage:

```python
library = Library()

# Adding books to the catalog
library.add_book("Atomic Habits", "James Clear", "Self-Help")
library.add_book("The 5 Second Rule", "Mel Robbins", "Self-Help")
library.add_book("The Lean Startup", "Eric Ries", "Business")

# Displaying the catalog
library.display_books()

# Searching books
library.display_search_results("author", "Ja", partial_match=True)
print("SEARCH END")

# Sorting books
library.sort_books("title")
print("\nSorted Catalog START:")
library.display_books()

# Checking out and returning books
library.checkout_book("Atomic Habits", "User3")
library.display_books()

library.return_book("Atomic Habits", "User3")
library.display_books()

# Checking overdue books
library.check_overdue_books()
