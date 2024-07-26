import csv
import hashlib
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    hashed_password = hash_password(password)
    
    with open('users.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, hashed_password])
    
    print("User registered successfully!")

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)
    
    with open('users.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == hashed_password:
                print("Login successful!")
                return username
    
    print("Invalid username or password.")
    return None

def user_authentication():
    while True:
        print("User Authentication Menu:")
        print("1. Register")
        print("2. Log In")
        print("3. Return to Main Menu")
        choice = input("Choose an option: ")

        if choice == '1':
            register()
        elif choice == '2':
            user = login()
            if user:
                return user
        elif choice == '3':
            break
        else:
            print("Invalid choice. Try again.")

def add_room():
    room_number = input("Enter room number: ")
    room_type = input("Enter room type (single, double, suite): ")
    price_per_night = input("Enter price per night: ")
    
    with open('rooms.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([room_number, room_type, price_per_night])
    
    print("Room added successfully!")

def view_rooms():
    with open('rooms.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(f"Room Number: {row[0]}, Type: {row[1]}, Price per Night: {row[2]}")

def edit_room():
    room_number = input("Enter the room number to edit: ")
    updated_type = input("Enter new room type (single, double, suite): ")
    updated_price = input("Enter new price per night: ")

    rooms = []

    with open('rooms.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == room_number:
                rooms.append([room_number, updated_type, updated_price])
            else:
                rooms.append(row)

    with open('rooms.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rooms)

    print("Room updated successfully!")

def delete_room():
    room_number = input("Enter the room number to delete: ")

    rooms = []

    with open('rooms.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != room_number:
                rooms.append(row)

    with open('rooms.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rooms)

    print("Room deleted successfully!")

def room_management():
    while True:
        print("Room Management Menu:")
        print("1. Add Room")
        print("2. View Rooms")
        print("3. Edit Room")
        print("4. Delete Room")
        print("5. Return to Main Menu")
        choice = input("Choose an option: ")

        if choice == '1':
            add_room()
        elif choice == '2':
            view_rooms()
        elif choice == '3':
            edit_room()
        elif choice == '4':
            delete_room()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Try again.")

def book_room(user_id):
    room_number = input("Enter room number: ")
    check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
    check_out_date = input("Enter check-out date (YYYY-MM-DD): ")

    with open('bookings.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, room_number, check_in_date, check_out_date])
    
    print("Room booked successfully!")

def view_bookings(user_id):
    with open('bookings.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == user_id:
                print(f"Booking ID: {reader.line_num}, Room Number: {row[1]}, Check-in Date: {row[2]}, Check-out Date: {row[3]}")

def cancel_booking(user_id):
    booking_id = input("Enter booking ID to cancel: ")
    bookings = []

    with open('bookings.csv', mode='r') as file:
        reader = csv.reader(file)
        for index, row in enumerate(reader, start=1):
            if row[0] == user_id and str(index) == booking_id:
                continue
            bookings.append(row)

    with open('bookings.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(bookings)

    print("Booking cancelled successfully!")

def booking_management():
    while True:
        print("Booking Management Menu:")
        print("1. Book Room")
        print("2. View Bookings")
        print("3. Cancel Booking")
        print("4. Return to Main Menu")
        choice = input("Choose an option: ")

        if choice == '1':
            user_id = input("Enter your user ID: ")
            book_room(user_id)
        elif choice == '2':
            user_id = input("Enter your user ID: ")
            view_bookings(user_id)
        elif choice == '3':
            user_id = input("Enter your user ID: ")
            cancel_booking(user_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

def total_bookings_over_period():
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    total_bookings = 0

    with open('bookings.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            check_in_date = datetime.strptime(row[2], "%Y-%m-%d")
            check_out_date = datetime.strptime(row[3], "%Y-%m-%d")
            if check_in_date >= start_date and check_out_date <= end_date:
                total_bookings += 1

    print(f"Total bookings from {start_date.date()} to {end_date.date()}: {total_bookings}")

def bookings_by_room_type():
    room_type_count = {}

    with open('rooms.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            room_type = row[1]
            room_type_count[room_type] = 0

    with open('bookings.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            room_number = row[1]
            with open('rooms.csv', mode='r') as room_file:
                room_reader = csv.reader(room_file)
                for room_row in room_reader:
                    if room_row[0] == room_number:
                        room_type = room_row[1]
                        room_type_count[room_type] += 1

    for room_type, count in room_type_count.items():
        print(f"Room Type: {room_type}, Bookings: {count}")

def user_booking_history():
    user_id = input("Enter user ID: ")
    
    with open('bookings.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == user_id:
                print(f"Booking ID: {reader.line_num}, Room Number: {row[1]}, Check-in Date: {row[2]}, Check-out Date: {row[3]}")

def generate_reports():
    while True:
        print("Reports Menu:")
        print("1. Total Bookings Over a Period")
        print("2. Bookings by Room Type")
        print("3. User-Specific Booking History")
        print("4. Return to Main Menu")
        choice = input("Choose an option: ")

        if choice == '1':
            total_bookings_over_period()
        elif choice == '2':
            bookings_by_room_type()
        elif choice == '3':
            user_booking_history()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

def main_menu():
    while True:
        print("Main Menu:")
        print("1. User Authentication")
        print("2. Room Management")
        print("3. Booking Management")
        print("4. Reports")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            user_authentication()
        elif choice == '2':
            room_management()
        elif choice == '3':
            booking_management()
        elif choice == '4':
            generate_reports()
        elif choice == '5':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
