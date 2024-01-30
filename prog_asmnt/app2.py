# https://github.com/MarsX-2002/pdp_python/tree/main/prog_asmnt

# print("\033[91mTEST: This should be red\033[0m")
# print("\033[92mTEST: This should be green\033[0m")

# ANSI color codes for terminal text coloring
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def colored_input(prompt, color):
    return input(color + prompt + RESET)

# Dictionary to store menu items and their prices.
menu = {
    "Spaghetti": 10.99,
    "Burger": 8.99,
    "Plov": 9.99,
    "Lavash": 5.99,
    "Salad": 7.99,
    "Steak": 15.99,
    "Pizza": 11.99,
    "Kebab": 13.99,   
}

# Function to display the menu to the user.
def display_menu():
    print(RED + "Menu:" + RESET)
    for meal, price in menu.items():
        print(RED + f"{meal}: ${price:.2f}" + RESET)  # Output in red

# 2. Reservation booking
reservations = {}  # Dictionary to store all reservations.

def book_table():
    """
    Book a reservation by getting customer name, number of guests, 
    selected meals, and table number. Validate input data. 
    Display menu, collect meal selections. Add reservation to 
    reservations dict. Print confirmation or error message.
    """
    try:
        customer_name = colored_input("Enter your name: ", GREEN)  
        guest_count = int(colored_input("Enter number of guests: ", GREEN))  
    except ValueError as e:
        print(RED + "Invalid number of guests. Please enter a valid number." + RESET)
        return

    display_menu()
    meals = []
    for _ in range(guest_count):
        try:
            meal = colored_input("Select a meal for each guest: ", GREEN) 
            while meal not in menu:
                print(RED + "Invalid meal selection. Please choose again." + RESET) 
                meal = colored_input("Select a meal for each guest: ", GREEN)  
            meals.append(meal)
        except ValueError as e:
            print(RED + f"An error occurred: {e}" + RESET)
            return
    
    try:
        table_number = colored_input("Enter table number: ", GREEN)  
        reservations[table_number] = {
            "Customer": customer_name,
            "Guests": guest_count,
            "Meals": meals
        }
        print(RED + f"Reservation booked for {customer_name} at table {table_number}." + RESET)  # Output in red
    except Exception as e:
        print(RED + f"An error occurred while booking: {e}" + RESET)


# CRUD
# READ: Function to view all reservations.
def view_reservations():
    if not reservations:
        print(RED + "No reservations found." + RESET)  # Output in red
        return
    for table, details in reservations.items():
        print(RED + f"Table {table}: {details}" + RESET)  # Displaying each reservation.

# UPDATE: Function to update a reservation.
def update_reservation():
    table_number = colored_input("Enter table number to update: ", GREEN)  
    if table_number not in reservations:
        print(RED + "Reservation not found." + RESET)  
        return
    
    # Offering options to update different aspects of the reservation.
    print(RED + "Update Options: 1. Customer Name 2. Number of Guests 3. Meals 4. Table Number" + RESET)  # Output in red
    update_choice = colored_input("What would you like to update? (Enter the number): ", GREEN)  # Input in green

    if update_choice == "1":
        new_name = colored_input("Enter the new customer name: ", GREEN)  # Input in green
        reservations[table_number]["Customer"] = new_name
        print(RED + "Customer name updated." + RESET)  # Output in red

    elif update_choice == "2":
        new_guest_count = int(colored_input("Enter the new number of guests: ", GREEN))  # Input in green
        reservations[table_number]["Guests"] = new_guest_count
        print(RED + "Number of guests updated." + RESET)  # Output in red

    elif update_choice == "3":
        new_meals = []
        for _ in range(reservations[table_number]["Guests"]):
            meal = colored_input("Select a new meal for each guest: ", GREEN)  # Input in green
            while meal not in menu:
                print(RED + "Invalid meal selection. Please choose again." + RESET)  # Output in red
                meal = colored_input("Select a new meal for each guest: ", GREEN)  # Input in green
            new_meals.append(meal)
        reservations[table_number]["Meals"] = new_meals
        print(RED + "Meals updated." + RESET)  

    elif update_choice == "4":
        new_table_number = colored_input("Enter the new table number: ", GREEN)  # Input in green
        reservations[new_table_number] = reservations.pop(table_number)
        print(RED + "Table number updated." + RESET)  

    else:
        print(RED + "Invalid option selected." + RESET)  

# DELETE: Function to cancel a reservation.
def cancel_reservation():
    table_number = colored_input("Enter table number to cancel: ", GREEN)  # Input in green
    if table_number in reservations:
        del reservations[table_number]  # Removing the reservation from the dictionary.
        print(RED + f"Reservation at table {table_number} canceled." + RESET)  # Output in red
    else:
        print(RED + "Reservation not found." + RESET)  

# Function to calculate the total price of a reservation.
def calculate_total_price():
    table_number = colored_input("Enter table number to calculate price: ", GREEN)  # Input in green
    if table_number not in reservations:
        print(RED + "Reservation not found." + RESET)  
        return
    # Calculating the total price by summing up the prices of selected meals.
    total_price = sum(menu[meal] for meal in reservations[table_number]["Meals"])
    print(RED + f"Total price for table {table_number}: ${total_price:.2f}" + RESET)  

# Main function to run the reservation system.
def main():
    while True:
        # Displaying menu options to the user.
        print(RED + "\nRestaurant Reservation System" + RESET)  
        print(RED + "1. Book a table" + RESET)  
        print(RED + "2. View reservations" + RESET)
        print(RED + "3. Update a reservation" + RESET)
        print(RED + "4. Cancel a reservation" + RESET)
        print(RED + "5. Calculate total price" + RESET)
        print(RED + "6. Exit" + RESET)
        choice = colored_input("Enter your choice: ", GREEN)  # Input in green
        
        # Processing the user's choice.
        if choice == "1":
            book_table()
        elif choice == "2":
            view_reservations()
        elif choice == "3":
            update_reservation()
        elif choice == "4":
            cancel_reservation()
        elif choice == "5":
            calculate_total_price()
        elif choice == "6":
            break  # Exiting the loop to end the program.
        else:
            print(RED + "Invalid choice. Please try again." + RESET)  # Output in red

if __name__ == "__main__":
    main()  # Starting the program.
