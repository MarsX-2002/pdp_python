import unittest
from app2 import colored_input, display_menu, book_table, view_reservations, update_reservation, cancel_reservation, calculate_total_price

class TestApp(unittest.TestCase):

    def test_colored_input(self):
        # Test valid input
        prompt = "Test prompt"
        color = "\033[92m"
        expected = color + prompt + "\033[0m"
        actual = colored_input(prompt, color)
        self.assertEqual(expected, actual)

        # Test invalid color code
        invalid_color = "\033[999m" 
        with self.assertRaises(ValueError):
            colored_input(prompt, invalid_color)

    def test_display_menu(self):
        # Test menu is displayed
        display_menu()
        # Menu display output cannot be easily tested

    def test_book_table(self):
        # Test valid booking
        customer = "John Doe"
        guests = 2
        meals = ["Burger", "Pizza"]
        table = "1"
        book_table(customer, guests, meals, table)
        self.assertIn(table, reservations)
        self.assertEqual(reservations[table]["Customer"], customer)
        
        # Test invalid guest number
        with self.assertRaises(ValueError):
            book_table(customer, "invalid", meals, table)

        # Test invalid meal selection
        with self.assertRaises(ValueError):
            book_table(customer, guests, ["Invalid"], table)

    def test_view_reservations(self):
        # Test with no reservations
        view_reservations()
        
        # Test with reservations
        book_table("Test", 2, ["Burger", "Pizza"], "2")
        view_reservations()
        # Output cannot be easily tested

    def test_update_reservation(self):
        # Test update name
        book_table("John Doe", 2, ["Burger", "Pizza"], "1")
        update_reservation("1", "name", "Jane Doe")
        self.assertEqual(reservations["1"]["Customer"], "Jane Doe")

        # Test update guests
        update_reservation("1", "guests", 3)
        self.assertEqual(reservations["1"]["Guests"], 3)

        # Test update meals
        update_reservation("1", "meals", ["Salad", "Pasta"])
        self.assertEqual(reservations["1"]["Meals"], ["Salad", "Pasta"])

        # Test update table
        update_reservation("1", "table", "2")
        self.assertIn("2", reservations)
        self.assertNotIn("1", reservations)

        # Test invalid reservation
        with self.assertRaises(KeyError):
            update_reservation("invalid", "name", "Test")

    def test_cancel_reservation(self):
        book_table("Test", 2, ["Burger", "Pizza"], "1")
        
        # Test cancel existing
        cancel_reservation("1")
        self.assertNotIn("1", reservations)

        # Test cancel non-existing
        cancel_reservation("invalid")

    def test_calculate_total_price(self):
        book_table("Test", 2, ["Burger", "Pizza"], "1")
        
        # Test valid calculation
        self.assertEqual(calculate_total_price("1"), 20.98)

        # Test invalid reservation
        with self.assertRaises(KeyError):
            calculate_total_price("invalid")

if __name__ == '__main__':
    unittest.main()