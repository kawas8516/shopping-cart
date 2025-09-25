-- PostgreSQL setup script for Shopping Cart Application

-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    mobile VARCHAR(15) NOT NULL UNIQUE,
    dob DATE,
    email VARCHAR(100),
    points INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create invoices table
CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    invoice_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount NUMERIC(10, 2) NOT NULL,
    discount_percentage NUMERIC(5, 2) DEFAULT 0,
    final_amount NUMERIC(10, 2) NOT NULL
);

-- Create invoice_items table
CREATE TABLE IF NOT EXISTS invoice_items (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id),
    item_name VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    total NUMERIC(10, 2) NOT NULL
);

-- Create employees table
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(100) NOT NULL,
    totp_secret VARCHAR(32),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default admin user
-- Default password is 'admin123' (this is just for initial setup, should be changed)
INSERT INTO employees (username, password_hash, is_admin)
VALUES ('admin', 'pbkdf2:sha256:150000$lLVMVvuP$b1d4b08d2d43a3d40296e7f462798d8b9344bf7e89e9e107bf3b4648a4d74f5b', TRUE)
ON CONFLICT (username) DO NOTHING;

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_customers_mobile ON customers(mobile);
CREATE INDEX IF NOT EXISTS idx_invoices_customer_id ON invoices(customer_id);
CREATE INDEX IF NOT EXISTS idx_invoice_items_invoice_id ON invoice_items(invoice_id);

-- Grant permissions (adjust as needed based on your PostgreSQL user)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_user;

COMMIT;

-- Note: Before running this script, create a database for your application
-- Example: CREATE DATABASE shopping_cart;
-- Then connect to that database and run this script