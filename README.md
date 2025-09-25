# Shopping Cart Application

## Overview
This is a comprehensive shopping cart application built with Python and Tkinter. It provides a user-friendly interface for managing sales, customer information, and employee operations in a retail environment.

## Features

### Customer Management
- Add customer information directly from Bill tab (name, mobile number, date of birth, email)
- Customer data integrated with billing and reward system
- View customer purchase history through Invoice History

### Shopping Cart
- Add items with name, quantity, and price
- View cart contents in a tabular format
- Reset cart functionality

### Billing System
- Calculate bill with subtotal, discount, and final amount
- Load existing customer info by mobile number for discounts
- Add new customer info directly from bill tab
- Save invoices to database
- Save bills as text files
- Send bills to customers via email
- Refresh bill calculation after customer changes

### Reward System
- Automatic points calculation (10 points per ₹100 spent)
- Reward tiers (Bronze, Silver, Gold) with increasing discounts
- Points tracking for each customer

### Master Employee Panel
- Always accessible (no authentication required)
- Sales reports by date range
- Top selling items analysis
- Customer management and search
- Email configuration for sending bills

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

### Dependencies
- Python 3.x
- Tkinter (GUI)
- PostgreSQL (Database)
- psycopg2 (PostgreSQL adapter)

### Database Schema
- **customers**: Customer information and reward points
- **invoices**: Sales transaction records
- **invoice_items**: Individual items in each invoice
- **employees**: Employee accounts with authentication details

## Usage

1. Run the application:
   ```
   python main.py
   ```

3. Use the tabs to navigate between different functions:
    - **Add Item**: Add products to the cart
    - **View Cart**: See current cart contents
    - **Bill**: Calculate and save invoices, add customer info
    - **Invoice History**: View past transactions by mobile search
    - **Employee Panel**: Access admin features (always available)

4. Billing Workflow:
    - Add items to cart
    - In Bill tab, optionally load existing customer by mobile number
    - Or add new customer info using "Add Customer Info" button
    - Click "Calculate Bill" to see bill with discounts
    - Use "Refresh Bill" if customer info is changed
    - Save invoice and optionally send by email
    - Save bill as text file using "Save Bill to File"

5. Email Configuration:
    - Go to Employee Panel
    - Click on "Configure Email" button
    - Enter your Gmail address and app password (not your regular Gmail password)
    - Gmail requires an app password for this type of integration

## Security Features

- Secure email configuration with app passwords
- Input validation for all user inputs
- PostgreSQL database with proper data types and constraints
- Customer data privacy and secure storage

## Future Enhancements

### Critical Missing Functions
- **Employee Panel**: Complete implementation of employee management interface (currently partially implemented)
- **Unified Storage System**: Resolve dual invoice storage (database + in-memory) inconsistency
- **Authentication System**: Implement employee login/logout with password hashing
- **Sales Reports**: Complete sales reporting functionality with date range analysis

### Planned Features
- **PDF Bill Generation**: Generate and email PDF invoices
- **Inventory Management**: Item catalog with stock tracking and low-stock alerts
- **Advanced Reporting**: Daily/weekly/monthly sales analytics and customer insights
- **Data Management**: Backup/restore, export/import capabilities
- **User Experience**: Dark mode, keyboard shortcuts, better error handling
- **Advanced Features**: Barcode scanning, receipt printing, multi-currency support
- **Quality Assurance**: Unit tests, integration tests, comprehensive logging

### Code Quality Improvements
- **Architecture**: Implement proper MVC separation and service layer
- **Error Handling**: Enhanced exception handling and user feedback
- **Configuration**: Environment-based settings and secure credential management
- **Documentation**: Complete API documentation and user guides

### Priority Implementation Roadmap
1. Fix Employee Panel and core missing functions
2. Implement authentication and security enhancements
3. Add PDF generation and complete billing workflow
4. Build inventory management system
5. Enhance reporting and analytics
6. Improve UI/UX and add advanced features
7. Implement testing and documentation