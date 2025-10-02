# Shopping Cart Application

A comprehensive shopping cart application built with Python and Tkinter for managing retail sales, customer information, and employee operations.
[Contributing](#contributing) | [Future Enhancements](#future-enhancements)

## Installation

1. Ensure Python 3.x is installed on your system.

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Database Setup:
   - Install PostgreSQL and create a database named 'shopping_cart'
   - Run the SQL commands in `postgresql_setup.sql` to create the necessary tables
   - Update database connection settings in `config.py` if needed

## Usage

1. Run the application:
   ```
   python main.py
   ```

2. Use the tabs to navigate between different functions:
   - **Add Item**: Add products to the cart
   - **View Cart**: See current cart contents
   - **Bill**: Calculate and save invoices, add customer info
   - **Invoice History**: View past transactions by mobile search
   - **Employee Panel**: Access admin features (always available)

## Features

- Customer management with reward points system
- Shopping cart with item addition and billing
- Invoice generation and email sending
- Employee panel for sales reports and customer search
- Secure data storage with PostgreSQL

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## Project Structure

```
shopping_cart/
├── main.py                 # Main entry point
├── controller.py           # Application controller
├── models.py               # Database models and operations
├── ui.py                   # User interface components
├── utils.py                # Utility functions and classes
├── email_service.py        # Email functionality
├── config.py               # Configuration settings
├── postgresql_setup.sql    # PostgreSQL setup script
├── requirements.txt        # Project dependencies
├── insert_sample_data.py   # Sample data insertion script
├── test_autocomplete.py    # Autocomplete testing script
└── database/               # Database directory
```

## Technical Details

- **Dependencies**: Python 3.x, Tkinter, PostgreSQL, psycopg2
- **Database Schema**: customers, invoices, invoice_items, employees

## Security Features

- Secure email configuration with app passwords
- Input validation and data privacy
- PostgreSQL with proper constraints

## Future Enhancements

- Complete employee panel implementation
- Authentication system
- PDF bill generation
- Inventory management
- Advanced reporting and UI improvements