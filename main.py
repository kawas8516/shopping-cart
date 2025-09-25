# main.py - Main entry point for the shopping cart application

from controller import ShoppingCartController
from config import DB_CONFIG, EMAIL_CONFIG, APP_SETTINGS

def main():
    # Create controller and run application with configuration
    app = ShoppingCartController(db_config=DB_CONFIG, email_config=EMAIL_CONFIG)
    app.run()

if __name__ == "__main__":
    main()