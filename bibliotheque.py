#CONSTANTS
LIBRARY_FILE = "library.txt"
STATUS_AVAILABLE = "Available"
STATUS_LOANED = "Loaned"
#Global inventory
inventory = []

#SECTION 1: FILE MANAGEMENT

def load_inventory():
    global inventory #modifying the inventory
    try:
        file = open(LIBRARY_FILE, 'r', encoding='utf-8')
        lines = file.readlines()
        file.close()
        inventory = []
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 5:
                    book = {
                        "Title": parts[0],
                        "Author": parts[1],
                        "Year": parts[2],
                        "ISBN": parts[3],
                        "Status": parts[4]
                    }
                    inventory.append(book)
        print(f"{len(inventory)} book(s) loaded successfully!")
        
    except FileNotFoundError:
        print("No file found. Starting with empty inventory.")
        inventory = []
    except PermissionError:
        print("Error: Permission denied to read the file.")
        inventory = []
    except Exception as e: #cathes any other error
        print(f"Unexpected error during loading: {e}")
        inventory = []

def save_inventory():
    try:
        file = open(LIBRARY_FILE, 'w', encoding='utf-8') #overwriting the existing content
        for book in inventory:
            line = f"{book['Title']}|{book['Author']}|{book['Year']}|{book['ISBN']}|{book['Status']}\n"
            file.write(line)
        file.close()
        print("Inventory saved successfully!")
        input("\nPress Enter to continue...")
        
    except PermissionError:
        print("Error: Permission denied to write to file.")
    except Exception as e:
        print(f"Error during saving: {e}")
        
#SECTION 2: UTILITY FUNCTIONS

def isbn_exists(isbn):
    for book in inventory:
        if book["ISBN"] == isbn:
            return True
    return False

def find_book_by_isbn(isbn):
    for book in inventory:
        if book["ISBN"] == isbn:
            return book
    return None

def validate_year(year_str):
    try:
        year = int(year_str)
        if 1000 <= year <= 2026:
            return True
        else:
            print("Year must be between 1000 and 2026!")
            return False
    except ValueError:
        print("Year must be a number!")
        return False
    
def validate_isbn(isbn):
    isbn_clean = isbn.replace("-", "").replace(" ", "")
    if len(isbn_clean) < 10:
        print("ISBN must contain at least 10 characters!")
        return False
    if not isbn_clean.isdigit():
        print("ISBN must contain only digits!")
        return False
    return True

#SECTION 3: BOOK CREATION AND MANAGEMENT

def create_book():
    print("          ADD A NEW BOOK")
    title = input("Book title: ").strip() #input & validation
    if not title:
        print("Title cannot be empty!")
        return None
    author = input("Author: ").strip()
    if not author:
        print("Author cannot be empty!")
        return None
    while True:
        year = input("Publication year: ").strip()
        if validate_year(year):
            break
    while True:
        isbn = input("ISBN: ").strip()
        if not validate_isbn(isbn):
            retry = input("Do you want to try again? (y/n): ").strip().lower()
            if retry != 'y':
                return None
        elif isbn_exists(isbn):
            print(f"Error: A book with ISBN {isbn} already exists!")
            return None
        else:
            break
    book = { #create dictionnary
        "Title": title,
        "Author": author,
        "Year": year,
        "ISBN": isbn,
        "Status": STATUS_AVAILABLE
    }
    return book

def add_book():
    book = create_book()
    if book:
        inventory.append(book)
        print(f"\nBook '{book['Title']}' added successfully!")
        save_inventory()
    else:
        print("\nBook addition cancelled.")
    
    input("\nPress Enter to continue...")

#SECTION 4: DISPLAY

def display_inventory():
    print("                    LIBRARY INVENTORY")
    if not inventory:
        print("\nInventory is empty. No books to display.")
        input("\nPress Enter to continue...")
        return
    print(f"\nTotal number of books: {len(inventory)}")
    
    for i in range(len(inventory)):
        book = inventory[i]
        if book['Status'] == STATUS_AVAILABLE:
            status_symbol = ":)"
        else:
            status_symbol = ":("
        
        print(f"\nBook {i + 1}:")
        print(f"   Title  : {book['Title']}")
        print(f"   Author : {book['Author']}")
        print(f"   Year   : {book['Year']}")
        print(f"   ISBN   : {book['ISBN']}")
        print(f"   Status : {book['Status']} {status_symbol}")
    input("\nPress Enter to continue...")

#SECTION 5: SEARCH

def search_book():
    print("              SEARCH FOR A BOOK")
    print("1. Search by title")
    print("2. Search by author")
    print("0. Back")
    
    choice = input("\nYour choice: ").strip()
    if choice == "0":
        return
    if choice not in ["1", "2"]:
        print("Invalid choice!")
        input("\nPress Enter to continue...")
        return
    search_term = input("Search term: ").strip().lower()
    if not search_term:
        print("Search term cannot be empty!")
        input("\nPress Enter to continue...")
        return

    results = []
    for book in inventory:
        if choice == "1":
            if search_term in book["Title"].lower():
                results.append(book)
        else:
            if search_term in book["Author"].lower():
                results.append(book)
    if not results:
        print("\nNo books found.")
        input("\nPress Enter to continue...")
        return
    print(f"\n{len(results)} book(s) found:")
    
    for i in range(len(results)):
        book = results[i]
        if book['Status'] == STATUS_AVAILABLE:
            status_symbol = ":)"
        else:
            status_symbol = ":("
        print(f"\n{i + 1}. {book['Title']}")
        print(f"  Author : {book['Author']}")
        print(f"  Year : {book['Year']}")
        print(f"  ISBN   : {book['ISBN']}")
        print(f"  Status : {book['Status']} {status_symbol}")
    input("\nPress Enter to continue...")

#SECTION 6: LOAN AND RETURN

def loan_book():
    print("              LOAN A BOOK")
    isbn = input("\nISBN of book to loan: ").strip()
    if not isbn:
        print("ISBN cannot be empty!")
        input("\nPress Enter to continue...")
        return
    
    book = find_book_by_isbn(isbn)
    if not book:
        print(f"No book found with ISBN: {isbn}")
        input("\nPress Enter to continue...")
        return
    if book["Status"] == STATUS_LOANED: #checking availability
        print(f"The book '{book['Title']}' is already loaned!")
        input("\nPress Enter to continue...")
        return
    book["Status"] = STATUS_LOANED #changing the status
    print(f"\nThe book '{book['Title']}' has been marked as loaned.")
    save_inventory()
    input("\nPress Enter to continue...")

def return_book():
    print("              RETURN A BOOK")
    isbn = input("\nISBN of book to return: ").strip()
    if not isbn:
        print("ISBN cannot be empty!")
        input("\nPress Enter to continue...")
        return
    
    book = find_book_by_isbn(isbn)
    if not book:
        print(f"No book found with ISBN: {isbn}")
        input("\nPress Enter to continue...")
        return
    if book["Status"] == STATUS_AVAILABLE:
        print(f"The book '{book['Title']}' is already available!")
        input("\nPress Enter to continue...")
        return
    book["Status"] = STATUS_AVAILABLE
    print(f"\nThe book '{book['Title']}' has been marked as available.")
    save_inventory()
    input("\nPress Enter to continue...")

#SECTION 7: DELETION

def delete_book():
    print("              DELETE A BOOK")
    isbn = input("\nISBN of book to delete: ").strip()
    if not isbn:
        print("ISBN cannot be empty!")
        input("\nPress Enter to continue...")
        return

    book = find_book_by_isbn(isbn)
    if not book:
        print(f"No book found with ISBN: {isbn}")
        input("\nPress Enter to continue...")
        return

    print("\nBook to delete:")
    print(f"   Title  : {book['Title']}")
    print(f"   Author : {book['Author']}")
    print(f"   ISBN   : {book['ISBN']}")
    confirmation = input("\nAre you sure you want to delete this book? (y/n): ").strip().lower()
    if confirmation == 'y':
        inventory.remove(book)
        print(f"\nThe book '{book['Title']}' has been deleted successfully.")
        save_inventory()
    else:
        print("\nDeletion cancelled.")
    input("\nPress Enter to continue...")

#SECTION 8: MAIN MENU

def display_menu():
    print("       DIGITAL LIBRARY - MAIN MENU")
    print("1. Add a book")
    print("2. Display inventory")
    print("3. Search for a book")
    print("4. Loan a book")
    print("5. Return a book")
    print("6. Delete a book")
    print("7. Save")
    print("8. Quit")

def main():
    print("     DIGITAL LIBRARY INVENTORY MANAGER")
    print("            Prep TIC - 2025/2026")
    load_inventory()
    
    while True: #loop
        try:
            display_menu()
            choice = input("\nYour choice: ").strip()
            if choice == "1":
                add_book()
            elif choice == "2":
                display_inventory()
            elif choice == "3":
                search_book()
            elif choice == "4":
                loan_book()
            elif choice == "5":
                return_book()
            elif choice == "6":
                delete_book()
            elif choice == "7":
                save_inventory()
            elif choice == "8":
                print("\nFinal save in progress...")
                save_inventory()
                print("\nThank you for using the library manager!")
                print("Goodbye! \n")
                break
            else:
                print("\nInvalid choice! Please choose between 1 and 9.")
        
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("The program continues...")
        
#Entry Point
if __name__ == "__main__":
    main()