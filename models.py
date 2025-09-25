# models.py - PostgreSQL database models and operations

import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime

class Database:
    def __init__(self, db_config=None):
        """Initialize PostgreSQL database connection"""
        try:
            if db_config is None:
                db_config = {
                    'host': 'localhost',
                    'port': 5432,
                    'database': 'shopping_cart',
                    'user': 'postgres',
                    'password': ''
                }

            self.conn = psycopg2.connect(
                host=db_config.get('host', 'localhost'),
                port=db_config.get('port', 5432),
                dbname=db_config.get('database', 'shopping_cart'),
                user=db_config.get('user', 'postgres'),
                password=db_config.get('password', '')
            )
            self.conn.autocommit = False
            self.cursor = self.conn.cursor(cursor_factory=DictCursor)
            print("Connected to PostgreSQL database")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise

    def setup_database(self):
        """Setup PostgreSQL database tables"""
        try:
            # Create customers table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    mobile TEXT UNIQUE NOT NULL,
                    dob TEXT,
                    email TEXT,
                    points INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create invoices table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoices (
                    id SERIAL PRIMARY KEY,
                    customer_id INTEGER,
                    total_amount NUMERIC(10,2) NOT NULL,
                    discount_amount NUMERIC(10,2) NOT NULL,
                    final_amount NUMERIC(10,2) NOT NULL,
                    bill_content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers (id)
                )
            """)

            # Create invoice items table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoice_items (
                    id SERIAL PRIMARY KEY,
                    invoice_id INTEGER NOT NULL,
                    item_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price NUMERIC(10,2) NOT NULL,
                    total NUMERIC(10,2) NOT NULL,
                    FOREIGN KEY (invoice_id) REFERENCES invoices (id)
                )
            """)

            # Create employees table (kept for potential future use, but not used in current flow)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    secret_key TEXT NOT NULL,
                    is_admin BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Commit changes
            self.conn.commit()
            print("Database tables created successfully")

        except Exception as e:
            self.conn.rollback()
            print(f"Error setting up database: {e}")
            raise

    def save_customer(self, name, mobile, dob, email=None):
        """Save customer information to database"""
        try:
            # Check if customer already exists
            self.cursor.execute("SELECT id FROM customers WHERE mobile = %s", (mobile,))
            existing_customer = self.cursor.fetchone()

            if existing_customer:
                # Update existing customer
                if email:
                    self.cursor.execute("""
                        UPDATE customers
                        SET name = %s, dob = %s, email = %s
                        WHERE mobile = %s
                    """, (name, dob, email, mobile))
                else:
                    self.cursor.execute("""
                        UPDATE customers
                        SET name = %s, dob = %s
                        WHERE mobile = %s
                    """, (name, dob, mobile))
                customer_id = existing_customer[0]
            else:
                # Insert new customer
                self.cursor.execute("""
                    INSERT INTO customers (name, mobile, dob, email)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (name, mobile, dob, email))
                customer_id = self.cursor.fetchone()[0]

            self.conn.commit()
            return customer_id

        except Exception as e:
            self.conn.rollback()
            print(f"Database error: {e}")
            return None

    def save_invoice(self, customer_mobile, total_amount, discount_amount, final_amount, cart, bill_content=None):
        """Save invoice and items to database"""
        try:
            # Get customer ID if mobile is provided
            customer_id = None
            if customer_mobile:
                self.cursor.execute("SELECT id FROM customers WHERE mobile = %s", (customer_mobile,))
                customer_result = self.cursor.fetchone()
                if customer_result:
                    customer_id = customer_result[0]

            # Insert invoice
            self.cursor.execute("""
                INSERT INTO invoices (customer_id, total_amount, discount_amount, final_amount, bill_content)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (customer_id, total_amount, discount_amount, final_amount, bill_content))

            invoice_id = self.cursor.fetchone()[0]

            # Insert invoice items
            for item in cart:
                self.cursor.execute("""
                    INSERT INTO invoice_items (invoice_id, item_name, quantity, price, total)
                    VALUES (%s, %s, %s, %s, %s)
                """, (invoice_id, item['name'], item['quantity'], item['price'], item['total']))

            # Update customer points if customer exists
            if customer_id:
                points_earned = int(final_amount / 100) * 10  # 10 points per ₹100

                self.cursor.execute("""
                    UPDATE customers
                    SET points = points + %s
                    WHERE id = %s
                """, (points_earned, customer_id))

            self.conn.commit()
            return invoice_id

        except Exception as e:
            self.conn.rollback()
            print(f"Database error: {e}")
            return None

    def get_customer_by_mobile(self, mobile):
        """Get customer by mobile number"""
        try:
            self.cursor.execute("SELECT id, name, mobile, dob, email, points FROM customers WHERE mobile = %s", (mobile,))
            customer = self.cursor.fetchone()

            if customer:
                return {
                    "id": customer[0],
                    "name": customer[1],
                    "mobile": customer[2],
                    "dob": customer[3],
                    "email": customer[4],
                    "points": customer[5]
                }
            else:
                return None

        except Exception as e:
            print(f"Database error: {e}")
            return None

    def get_invoices_by_mobile(self, mobile):
        """Get invoices for a customer by mobile number"""
        try:
            # Get customer ID
            self.cursor.execute("SELECT id FROM customers WHERE mobile = %s", (mobile,))
            customer = self.cursor.fetchone()

            if not customer:
                return []

            customer_id = customer[0]

            # Get invoices
            self.cursor.execute("""
                SELECT id, created_at, total_amount, discount_amount, final_amount
                FROM invoices
                WHERE customer_id = %s
                ORDER BY created_at DESC
            """, (customer_id,))

            invoices = self.cursor.fetchall()

            result = []
            for invoice in invoices:
                invoice_id, created_at, total, discount, final = invoice

                # Format date
                if isinstance(created_at, str):
                    date_obj = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                else:
                    date_obj = created_at
                formatted_date = date_obj.strftime("%d/%m/%Y %H:%M")

                result.append({
                    "id": invoice_id,
                    "date": formatted_date,
                    "total": total,
                    "discount": discount,
                    "final": final
                })

            return result

        except Exception as e:
            print(f"Database error: {e}")
            return []

    def get_invoice_details(self, invoice_id):
        """Get invoice details"""
        try:
            # Get invoice
            self.cursor.execute("""
                SELECT i.id, i.created_at, c.name, c.mobile, i.total_amount, i.discount_amount, i.final_amount
                FROM invoices i
                JOIN customers c ON i.customer_id = c.id
                WHERE i.id = %s
            """, (invoice_id,))

            invoice = self.cursor.fetchone()
            if not invoice:
                return None

            # Get invoice items
            self.cursor.execute("""
                SELECT item_name, quantity, price, total
                FROM invoice_items
                WHERE invoice_id = %s
            """, (invoice_id,))

            items = self.cursor.fetchall()

            # Format invoice details
            invoice_id, created_at, customer_name, mobile, total, discount, final = invoice

            # Format date
            if isinstance(created_at, str):
                date_obj = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            else:
                date_obj = created_at
            formatted_date = date_obj.strftime("%d/%m/%Y %H:%M")

            result = {
                "id": invoice_id,
                "date": formatted_date,
                "customer_name": customer_name,
                "mobile": mobile,
                "total": total,
                "discount": discount,
                "final": final,
                "items": []
            }

            for item in items:
                name, quantity, price, item_total = item
                result["items"].append({
                    "name": name,
                    "quantity": quantity,
                    "price": price,
                    "total": item_total
                })

            return result

        except Exception as e:
            print(f"Database error: {e}")
            return None

    def get_employee(self, username):
        """Get employee by username"""
        try:
            self.cursor.execute(
                "SELECT id, username, password_hash, salt, secret_key, is_admin FROM employees WHERE username = %s",
                (username,)
            )

            employee = self.cursor.fetchone()
            if not employee:
                return None

            return {
                "id": employee[0],
                "username": employee[1],
                "password_hash": employee[2],
                "salt": employee[3],
                "secret_key": employee[4],
                "is_admin": bool(employee[5])
            }

        except Exception as e:
            print(f"Database error: {e}")
            return None

    def generate_sales_report(self, from_date, to_date):
        """Get sales report for date range"""
        try:
            # Get sales data
            self.cursor.execute("""
                SELECT
                    COUNT(*) as invoice_count,
                    SUM(total_amount) as total_sales,
                    SUM(discount_amount) as total_discount,
                    SUM(final_amount) as final_sales
                FROM invoices
                WHERE created_at BETWEEN %s AND %s
            """, (from_date, to_date))

            sales_summary = self.cursor.fetchone()

            # Get top selling items
            self.cursor.execute("""
                SELECT
                    item_name,
                    SUM(quantity) as total_quantity,
                    SUM(total) as total_sales
                FROM invoice_items
                JOIN invoices ON invoice_items.invoice_id = invoices.id
                WHERE invoices.created_at BETWEEN %s AND %s
                GROUP BY item_name
                ORDER BY total_quantity DESC
                LIMIT 5
            """, (from_date, to_date))

            top_items = self.cursor.fetchall()

            # Format report data
            invoice_count, total_sales, total_discount, final_sales = sales_summary

            result = {
                "invoice_count": invoice_count or 0,
                "total_sales": total_sales or 0,
                "total_discount": total_discount or 0,
                "final_sales": final_sales or 0,
                "top_items": []
            }

            for item in top_items:
                name, quantity, sales = item
                result["top_items"].append({
                    "name": name,
                    "quantity": quantity,
                    "sales": sales
                })

            return result

        except Exception as e:
            print(f"Database error: {e}")
            return None

    def update_customer_points(self, mobile, points):
        """Update customer points"""
        try:
            self.cursor.execute("""
                UPDATE customers
                SET points = %s
                WHERE mobile = %s
            """, (points, mobile))

            self.conn.commit()
            return True

        except Exception as e:
            print(f"Database error: {e}")
            return False

    def search_customers(self, mobile=None):
        """Search customers by mobile number"""
        try:
            # Prepare query
            query = "SELECT id, name, mobile, dob, points, created_at FROM customers"
            params = ()

            if mobile:
                query += " WHERE mobile LIKE %s"
                params = (f"%{mobile}%",)

            query += " ORDER BY name"

            # Execute query
            self.cursor.execute(query, params)
            customers = self.cursor.fetchall()

            result = []
            for customer in customers:
                customer_id, name, mobile, dob, points, created_at = customer

                # Format date
                if isinstance(created_at, str):
                    date_obj = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                else:
                    date_obj = created_at
                formatted_date = date_obj.strftime("%d/%m/%Y")

                result.append({
                    "id": customer_id,
                    "name": name,
                    "mobile": mobile,
                    "dob": dob or "N/A",
                    "points": points,
                    "created_at": formatted_date
                })

            return result

        except Exception as e:
            print(f"Database error: {e}")
            return []

    def search_customers_by_name(self, name_prefix, limit=10):
        """Search customers by name prefix for autocomplete"""
        try:
            query = """
                SELECT DISTINCT name
                FROM customers
                WHERE LOWER(name) LIKE LOWER(%s)
                ORDER BY name
                LIMIT %s
            """
            self.cursor.execute(query, (f"{name_prefix}%", limit))
            results = self.cursor.fetchall()
            return [row[0] for row in results]

        except Exception as e:
            print(f"Database error: {e}")
            return []

    def search_customers_by_mobile(self, mobile_prefix, limit=10):
        """Search customers by mobile prefix for autocomplete"""
        try:
            query = """
                SELECT DISTINCT mobile
                FROM customers
                WHERE mobile LIKE %s
                ORDER BY mobile
                LIMIT %s
            """
            self.cursor.execute(query, (f"{mobile_prefix}%", limit))
            results = self.cursor.fetchall()
            return [row[0] for row in results]

        except Exception as e:
            print(f"Database error: {e}")
            return []

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")