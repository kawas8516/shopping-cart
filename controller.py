# controller.py - Controller for the shopping cart application

import tkinter as tk
from datetime import datetime

from email_service import EmailService
from models import Database
from utils import Validator, RewardSystem, PriceFormatter

class ShoppingCartController:
    def __init__(self, db_config=None, email_config=None):
        # Initialize cart and customer info
        self.cart = []
        self.customer_info = {
            "name": "",
            "mobile": "",
            "dob": "",
            "email": ""
        }
        self.current_user = {"username": "master", "is_admin": True}
        
        # Initialize Python-side invoice storage
        self.invoices = []  # Store invoices in memory
        self.invoice_counter = 1  # Counter for invoice IDs
        
        # Initialize database with configuration
        self.db = Database(db_config)
        self.db.setup_database()
        
        # Initialize email service with configuration
        self.email_service = EmailService(email_config)
        
        # Initialize UI
        self.root = tk.Tk()
        
        # Import UI here to avoid circular import
        from ui import ShoppingCartUI
        self.ui = ShoppingCartUI(self.root, self)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()
    
    def add_to_cart(self):
        """Add item to cart"""
        # Get values from UI
        name = self.ui.name_var.get().strip()
        quantity_str = self.ui.quantity_var.get().strip()
        price_str = self.ui.price_var.get().strip()
        
        # Validate inputs
        if not name:
            self.ui.status_var.set("Item name cannot be empty")
            return
        
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                self.ui.status_var.set("Quantity must be a positive number")
                return
        except ValueError:
            self.ui.status_var.set("Quantity must be a valid number")
            return
        
        try:
            price = float(price_str)
            if price <= 0:
                self.ui.status_var.set("Price must be a positive number")
                return
        except ValueError:
            self.ui.status_var.set("Price must be a valid number")
            return
        
        # Add to cart
        total = quantity * price
        self.cart.append({
            "name": name,
            "quantity": quantity,
            "price": price,
            "total": total
        })
        
        # Clear inputs
        self.ui.name_var.set("")
        self.ui.quantity_var.set("")
        self.ui.price_var.set("")
        self.ui.status_var.set(f"{name} added to cart")
        
        # Update cart view
        self.ui.update_cart_view(self.cart)
    
    def reset_cart(self):
        """Reset the cart"""
        # Confirm reset
        if not self.ui.ask_confirmation("Reset Cart", "Are you sure you want to reset the cart?"):
            return
        
        # Clear cart
        self.cart = []
        
        # Update cart view
        self.ui.update_cart_view(self.cart)
        
        # Clear bill
        self.ui.update_bill_view("")
    
    def calculate_bill(self):
        """Calculate the bill"""
        if not self.cart:
            self.ui.show_message("Empty Cart", "The cart is empty", error=True)
            return
        
        # Calculate totals
        subtotal = sum(item["total"] for item in self.cart)
        
        # Get customer info
        customer_name = self.customer_info.get("name", "")
        customer_mobile = self.customer_info.get("mobile", "")
        
        # Get reward tier and discount if customer exists
        discount = 0
        reward_tier = "None"
        
        if customer_mobile:
            # Get customer from database
            customer = self.db.get_customer_by_mobile(customer_mobile)
            if customer:
                # Calculate reward tier and discount
                points = customer["points"]
                reward_tier = RewardSystem.get_reward_tier(points)
                discount_percent = RewardSystem.get_discount_percentage(reward_tier)
                discount = subtotal * discount_percent
        
        # Calculate final amount
        final_amount = subtotal - discount
        
        # Format bill
        bill = PriceFormatter.format_bill(
            self.cart,
            subtotal,
            discount,
            final_amount,
            customer_name,
            customer_mobile,
            reward_tier
        )
        
        # Update bill view
        self.ui.update_bill_view(bill)
    
    def save_customer_info(self):
        """Save customer information"""
        # Get values from UI
        name = self.ui.customer_name_var.get().strip()
        mobile = self.ui.customer_mobile_var.get().strip()
        dob = self.ui.customer_dob_var.get().strip()
        email = self.ui.customer_email_var.get().strip() if hasattr(self.ui, 'customer_email_var') else ""

        # Validate inputs
        if not Validator.validate_name(name):
            self.ui.customer_status_var.set("Please enter a valid name")
            return

        if not Validator.validate_mobile(mobile):
            self.ui.customer_status_var.set("Please enter a valid 10-digit mobile number")
            return

        if not Validator.validate_date(dob):
            self.ui.customer_status_var.set("Please enter a valid date in DD/MM/YYYY format")
            return

        # Validate email if provided
        if email and not Validator.validate_email(email):
            self.ui.customer_status_var.set("Please enter a valid email address")
            return

        # Save to customer info dictionary
        self.customer_info = {
            "name": name,
            "mobile": mobile,
            "dob": dob,
            "email": email
        }

        # Save to database
        self.db.save_customer(name, mobile, dob, email)

        # Show success message
        self.ui.customer_status_var.set("Customer information saved successfully")


    def save_customer_info_from_bill(self, name, mobile, dob, email, status_var, dialog):
        """Save customer information from bill tab dialog"""
        # Validate inputs
        if not Validator.validate_name(name):
            status_var.set("Please enter a valid name")
            return

        if not Validator.validate_mobile(mobile):
            status_var.set("Please enter a valid 10-digit mobile number")
            return

        if not Validator.validate_date(dob):
            status_var.set("Please enter a valid date in DD/MM/YYYY format")
            return

        # Validate email if provided
        if email and not Validator.validate_email(email):
            status_var.set("Please enter a valid email address")
            return

        # Save to customer info dictionary
        self.customer_info = {
            "name": name,
            "mobile": mobile,
            "dob": dob,
            "email": email
        }

        # Save to database
        self.db.save_customer(name, mobile, dob, email)

        # Show success message
        status_var.set("Customer information added to bill successfully")

        # Close dialog
        dialog.destroy()
    
    def save_invoice(self):
        """Save the invoice to Python-side storage"""
        if not self.cart:
            self.ui.show_message("Empty Cart", "The cart is empty", error=True)
            return
        
        # Check if bill is calculated
        bill_text = self.ui.bill_text.get(1.0, tk.END).strip()
        if not bill_text:
            self.ui.show_message("Calculate Bill", "Please calculate the bill first", error=True)
            return
        
        # Get customer info
        customer_mobile = self.customer_info.get("mobile", "")
        customer_name = self.customer_info.get("name", "")
        customer_email = self.customer_info.get("email", "")
        
        # Calculate totals
        subtotal = sum(item["total"] for item in self.cart)
        
        # Get reward tier and discount if customer exists
        discount = 0
        
        if customer_mobile:
            # Get customer from database
            customer = self.db.get_customer_by_mobile(customer_mobile)
            if customer:
                # Calculate reward tier and discount
                points = customer["points"]
                reward_tier = RewardSystem.get_reward_tier(points)
                discount_percent = RewardSystem.get_discount_percentage(reward_tier)
                discount = subtotal * discount_percent
                
                # Calculate reward points for this purchase
                new_points = RewardSystem.calculate_points(subtotal - discount)
                
                # Update customer points in database
                self.db.update_customer_points(customer_mobile, points + new_points)
                
                # Update customer info with database values if needed
                if not customer_name:
                    customer_name = customer.get("name", "")
                if not customer_email:
                    customer_email = customer.get("email", "")
        
        # Calculate final amount
        final_amount = subtotal - discount
        
        # Create invoice object for Python-side storage
        invoice = {
            "id": self.invoice_counter,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer_name": customer_name,
            "customer_mobile": customer_mobile,
            "customer_email": customer_email,
            "subtotal": subtotal,
            "discount": discount,
            "total": final_amount,
            "items": [item.copy() for item in self.cart],  # Deep copy of cart items
            "bill_content": bill_text
        }
        
        # Save to Python-side storage
        self.invoices.append(invoice)
        invoice_id = self.invoice_counter
        self.invoice_counter += 1
        
        # Show success message
        self.ui.show_message("Invoice Saved", f"Invoice #{invoice_id} saved successfully")
        
        # Ask if user wants to send bill via email
        if customer_email and self.email_service.is_configured():
            if self.ui.ask_confirmation("Send Bill", f"Do you want to send the bill to {customer_email}?"):
                self.send_bill_by_email(customer_email, customer_name, bill_text, invoice_id)
        
        # Reset cart and customer info
        self.reset_cart()
        self.customer_info = {"name": "", "mobile": "", "dob": "", "email": ""}
        self.ui.customer_info_label.config(text="No customer info added", fg="#666666")
    
    
    def search_invoices(self):
        """Search invoices by mobile number"""
        # Get mobile number from UI
        mobile = self.ui.search_mobile_var.get().strip()
        
        if not mobile:
            self.ui.show_message("Search Error", "Please enter a mobile number", error=True)
            return
        
        # Get invoices from database
        invoices = self.db.get_invoices_by_mobile(mobile)
        
        # Update invoice view
        self.ui.update_invoice_view(invoices)
    
    def show_invoice_details(self, event):
        """Show invoice details"""
        # Get selected invoice
        selected_item = self.ui.invoice_tree.selection()
        if not selected_item:
            return
        
        # Get invoice ID
        invoice_id = self.ui.invoice_tree.item(selected_item[0], "values")[0]
        
        # Get invoice details from database
        invoice = self.db.get_invoice_details(invoice_id)
        
        # Update invoice details view
        self.ui.update_invoice_details(invoice)
    
    def save_bill_to_file(self):
        """Save bill content to a text file"""
        bill_content = self.ui.bill_text.get(1.0, tk.END).strip()
        if not bill_content:
            self.ui.show_message("No Bill", "Please calculate the bill first", error=True)
            return

        try:
            from tkinter import filedialog
            # Ask user for file location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Bill As"
            )

            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(bill_content)
                self.ui.show_message("Bill Saved", f"Bill saved successfully to {file_path}")
        except Exception as e:
            self.ui.show_message("Save Error", f"Error saving bill: {str(e)}", error=True)

    def send_bill_by_email(self, customer_email, customer_name, bill_content, invoice_id):
        """Send bill to customer via email"""
        try:
            # Format subject
            subject = f"Your Invoice #{invoice_id} - {self.ui.title_label['text']}"

            # Send email
            success = self.email_service.send_bill(
                recipient_email=customer_email,
                recipient_name=customer_name,
                subject=subject,
                bill_content=bill_content,
                invoice_id=invoice_id
            )

            if success:
                self.ui.show_message("Email Sent", f"Bill sent successfully to {customer_email}")
            else:
                self.ui.show_message("Email Error", "Failed to send email. Please check email configuration.", error=True)
        except Exception as e:
            self.ui.show_message("Email Error", f"Error sending email: {str(e)}", error=True)
    
    def configure_email_service(self, email, password, dialog):
        """Configure email service with Gmail credentials"""
        if not email or not password:
            self.ui.show_message("Configuration Error", "Email and password are required", error=True)
            return
        
        try:
            # Configure email service
            success = self.email_service.configure(email, password)
            
            if success:
                self.ui.show_message("Email Configuration", "Email configuration saved successfully")
                dialog.destroy()
            else:
                self.ui.show_message("Configuration Error", "Failed to configure email service", error=True)
        except Exception as e:
            self.ui.show_message("Configuration Error", f"Error configuring email: {str(e)}", error=True)
    
    def save_customer_info_from_bill(self, name, mobile, dob, email, status_var, dialog):
        """Save customer info from bill tab"""
        # Validate inputs
        if not name or not mobile:
            status_var.set("Name and mobile number are required")
            return
        
        # Validate mobile number
        if not Validator.validate_mobile(mobile):
            status_var.set("Invalid mobile number format")
            return
        
        # Validate DOB if provided
        if dob and not Validator.validate_date(dob):
            status_var.set("Invalid date format. Use DD/MM/YYYY")
            return
        
        # Validate email if provided
        if email and not Validator.validate_email(email):
            status_var.set("Invalid email format")
            return
        
        # Update customer info
        self.customer_info = {
            "name": name,
            "mobile": mobile,
            "dob": dob,
            "email": email
        }
        
        # Update UI label
        self.ui.customer_info_label.config(
            text=f"Customer: {name} ({mobile})",
            fg="#4CAF50"
        )
        
        status_var.set("Customer info added successfully!")
        dialog.destroy()
    
    def search_invoice_history(self, mobile, history_text):
        """Search and display invoice history for a mobile number"""
        if not mobile:
            history_text.config(state=tk.NORMAL)
            history_text.delete(1.0, tk.END)
            history_text.insert(tk.END, "Please enter a mobile number.")
            history_text.config(state=tk.DISABLED)
            return
        
        # Validate mobile number
        if not Validator.validate_mobile(mobile):
            history_text.config(state=tk.NORMAL)
            history_text.delete(1.0, tk.END)
            history_text.insert(tk.END, "Invalid mobile number format.")
            history_text.config(state=tk.DISABLED)
            return
        
        try:
            # Get invoices from Python-side storage (in-memory)
            invoices = self.get_invoices_by_mobile(mobile)
            
            history_text.config(state=tk.NORMAL)
            history_text.delete(1.0, tk.END)
            
            if not invoices:
                history_text.insert(tk.END, f"No invoice history found for mobile number: {mobile}")
            else:
                history_text.insert(tk.END, f"Invoice History for {mobile}\n")
                history_text.insert(tk.END, "=" * 50 + "\n\n")
                
                for invoice in invoices:
                    history_text.insert(tk.END, f"Invoice ID: {invoice['id']}\n")
                    history_text.insert(tk.END, f"Date: {invoice['date']}\n")
                    history_text.insert(tk.END, f"Customer: {invoice['customer_name']}\n")
                    history_text.insert(tk.END, f"Total: {PriceFormatter.format_price(invoice['total'])}\n")
                    history_text.insert(tk.END, f"Items: {len(invoice['items'])}\n")
                    history_text.insert(tk.END, "-" * 30 + "\n")
                    
                    for item in invoice['items']:
                        history_text.insert(tk.END, f"  {item['name']} x {item['quantity']} @ {PriceFormatter.format_price(item['price'])}\n")
                    
                    history_text.insert(tk.END, "\n")
            
            history_text.config(state=tk.DISABLED)
            
        except Exception as e:
            history_text.config(state=tk.NORMAL)
            history_text.delete(1.0, tk.END)
            history_text.insert(tk.END, f"Error searching invoice history: {str(e)}")
            history_text.config(state=tk.DISABLED)
    
    def get_invoices_by_mobile(self, mobile):
        """Get invoices by mobile number from Python-side storage"""
        matching_invoices = []
        for invoice in self.invoices:
            if invoice.get("customer_mobile") == mobile:
                matching_invoices.append(invoice)

        # Sort by date (newest first)
        matching_invoices.sort(key=lambda x: x["date"], reverse=True)
        return matching_invoices

    def get_customer_name_suggestions(self, prefix):
        """Get customer name suggestions for autocomplete"""
        return self.db.search_customers_by_name(prefix)

    def get_customer_mobile_suggestions(self, prefix):
        """Get customer mobile suggestions for autocomplete"""
        return self.db.search_customers_by_mobile(prefix)
    
    
    
    