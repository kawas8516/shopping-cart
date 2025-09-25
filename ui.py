# ui.py - User interface components for the shopping cart application

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import font as tkfont
from datetime import datetime, timedelta

from utils import PriceFormatter, RewardSystem

class ShoppingCartUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        # Configure root window
        self.root.title("Shopping Cart Application")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Set custom fonts
        self.title_font = tkfont.Font(family="Arial", size=16, weight="bold")
        self.header_font = tkfont.Font(family="Arial", size=12, weight="bold")
        self.normal_font = tkfont.Font(family="Arial", size=10)
        
        # Create main frame
        self.main_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create title
        self.title_label = tk.Label(
            self.main_frame, 
            text="Shopping Cart Application", 
            font=self.title_font, 
            bg="#f0f0f0", 
            fg="#333333"
        )
        self.title_label.pack(pady=(0, 20))
        
        # Create tab control
        self.tab_control = ttk.Notebook(self.main_frame)
        
        # Create tabs
        self.add_tab = tk.Frame(self.tab_control, bg="#f0f0f0")
        self.view_tab = tk.Frame(self.tab_control, bg="#f0f0f0")
        self.bill_tab = tk.Frame(self.tab_control, bg="#f0f0f0")
        self.history_tab = tk.Frame(self.tab_control, bg="#f0f0f0")

        # Add tabs to notebook
        self.tab_control.add(self.add_tab, text="Add Item")
        self.tab_control.add(self.view_tab, text="View Cart")
        self.tab_control.add(self.bill_tab, text="Bill")
        self.tab_control.add(self.history_tab, text="Invoice History")

        self.tab_control.pack(expand=1, fill="both")

        # Setup tabs
        self.setup_add_tab()
        self.setup_view_tab()
        self.setup_bill_tab()
        self.setup_history_tab()
    
    def setup_add_tab(self):
        """Setup the add item tab"""
        # Create frame for add item
        add_frame = tk.Frame(self.add_tab, bg="#f0f0f0", padx=20, pady=20)
        add_frame.pack(fill=tk.BOTH, expand=True)
        
        # Item name
        name_frame = tk.Frame(add_frame, bg="#f0f0f0")
        name_frame.pack(fill="x", pady=5)
        
        tk.Label(name_frame, text="Item Name:", font=self.normal_font, bg="#f0f0f0", width=15, anchor="w").pack(side="left")
        self.name_var = tk.StringVar()
        tk.Entry(name_frame, textvariable=self.name_var, font=self.normal_font, width=30).pack(side="left", padx=5)
        
        # Item quantity
        quantity_frame = tk.Frame(add_frame, bg="#f0f0f0")
        quantity_frame.pack(fill="x", pady=5)
        
        tk.Label(quantity_frame, text="Quantity:", font=self.normal_font, bg="#f0f0f0", width=15, anchor="w").pack(side="left")
        self.quantity_var = tk.StringVar()
        tk.Entry(quantity_frame, textvariable=self.quantity_var, font=self.normal_font, width=30).pack(side="left", padx=5)
        
        # Item price
        price_frame = tk.Frame(add_frame, bg="#f0f0f0")
        price_frame.pack(fill="x", pady=5)
        
        tk.Label(price_frame, text="Price (₹):", font=self.normal_font, bg="#f0f0f0", width=15, anchor="w").pack(side="left")
        self.price_var = tk.StringVar()
        tk.Entry(price_frame, textvariable=self.price_var, font=self.normal_font, width=30).pack(side="left", padx=5)
        
        # Add button
        add_button = tk.Button(
            add_frame, 
            text="Add to Cart", 
            command=self.controller.add_to_cart, 
            font=self.normal_font,
            bg="#4CAF50", 
            fg="white", 
            padx=20, 
            pady=5
        )
        add_button.pack(pady=20)
        
        # Status message
        self.status_var = tk.StringVar()
        status_label = tk.Label(add_frame, textvariable=self.status_var, font=self.normal_font, bg="#f0f0f0", fg="#F44336")
        status_label.pack(pady=10)
    
    def setup_view_tab(self):
        """Setup the view cart tab"""
        # Create frame for view cart
        view_frame = tk.Frame(self.view_tab, bg="#f0f0f0", padx=20, pady=20)
        view_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview for cart items
        columns = ("Item", "Quantity", "Price", "Total")
        self.cart_tree = ttk.Treeview(view_frame, columns=columns, show="headings", height=10)
        
        # Set column headings
        for col in columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=100, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(view_frame, orient="vertical", command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.cart_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create button frame
        button_frame = tk.Frame(view_frame, bg="#f0f0f0", pady=10)
        button_frame.pack(fill="x")
        
        # Reset cart button
        reset_button = tk.Button(
            button_frame, 
            text="Reset Cart", 
            command=self.controller.reset_cart, 
            font=self.normal_font,
            bg="#F44336", 
            fg="white", 
            padx=20, 
            pady=5
        )
        reset_button.pack(side="left", padx=10)
    
    def setup_bill_tab(self):
        """Setup the bill tab"""
        # Create frame for bill
        bill_frame = tk.Frame(self.bill_tab, bg="#f0f0f0", padx=20, pady=20)
        bill_frame.pack(fill=tk.BOTH, expand=True)
        
        # Customer info frame
        customer_info_frame = tk.Frame(bill_frame, bg="#f0f0f0")
        customer_info_frame.pack(fill="x", pady=(0, 10))
        
        # Customer info display label
        self.customer_info_label = tk.Label(
            customer_info_frame, 
            text="No customer info added", 
            font=self.normal_font, 
            bg="#f0f0f0", 
            fg="#666666"
        )
        self.customer_info_label.pack(side="left")

        # Create text widget for bill
        self.bill_text = tk.Text(bill_frame, height=20, width=70, font=self.normal_font)
        self.bill_text.pack(fill="both", expand=True)

        # Create button frame
        button_frame = tk.Frame(bill_frame, bg="#f0f0f0", pady=10)
        button_frame.pack(fill="x")

        # Add customer info button
        customer_button = tk.Button(
            button_frame,
            text="Add Customer Info (Optional)",
            command=self.show_customer_info_dialog,
            font=self.normal_font,
            bg="#9C27B0",
            fg="white",
            padx=20,
            pady=5
        )
        customer_button.pack(side="left", padx=10)

        # Calculate bill button
        calculate_button = tk.Button(
            button_frame,
            text="Calculate Bill",
            command=self.controller.calculate_bill,
            font=self.normal_font,
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=5
        )
        calculate_button.pack(side="left", padx=10)

        # View Invoice History button
        history_button = tk.Button(
            button_frame,
            text="View Invoice History",
            command=self.show_invoice_history_dialog,
            font=self.normal_font,
            bg="#FF5722",
            fg="white",
            padx=20,
            pady=5
        )
        history_button.pack(side="left", padx=10)

        # Save invoice button
        save_button = tk.Button(
            button_frame,
            text="Save Invoice",
            command=self.controller.save_invoice,
            font=self.normal_font,
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5
        )
        save_button.pack(side="left", padx=10)

        # Save bill to file button
        save_file_button = tk.Button(
            button_frame,
            text="Save Bill to File",
            command=self.controller.save_bill_to_file,
            font=self.normal_font,
            bg="#9C27B0",
            fg="white",
            padx=20,
            pady=5
        )
        save_file_button.pack(side="left", padx=10)

        # Send bill by email button
        email_button = tk.Button(
            button_frame,
            text="Send Bill by Email",
            command=self.controller.send_bill_by_email,
            font=self.normal_font,
            bg="#FF9800",
            fg="white",
            padx=20,
            pady=5
        )
        email_button.pack(side="left", padx=10)
    
    
    def setup_history_tab(self):
        """Setup the invoice history tab"""
        # Create frame for invoice history
        history_frame = tk.Frame(self.history_tab, bg="#f0f0f0", padx=20, pady=20)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create search frame
        search_frame = tk.Frame(history_frame, bg="#f0f0f0")
        search_frame.pack(fill="x", pady=(0, 10))
        
        # Mobile number search
        tk.Label(search_frame, text="Mobile Number:", font=self.normal_font, bg="#f0f0f0").pack(side="left", padx=5)
        self.search_mobile_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_mobile_var, font=self.normal_font, width=15).pack(side="left", padx=5)
        
        # Search button
        search_button = tk.Button(
            search_frame, 
            text="Search Invoices", 
            command=self.controller.search_invoices, 
            font=self.normal_font,
            bg="#2196F3", 
            fg="white", 
            padx=10, 
            pady=2
        )
        search_button.pack(side="left", padx=10)
        
        # Create treeview for invoices
        columns = ("Invoice ID", "Date", "Total Amount", "Discount", "Final Amount")
        self.invoice_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=8)
        
        # Set column headings
        for col in columns:
            self.invoice_tree.heading(col, text=col)
            self.invoice_tree.column(col, width=100, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.invoice_tree.yview)
        self.invoice_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.invoice_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click event to show invoice details
        self.invoice_tree.bind("<Double-1>", self.controller.show_invoice_details)
        
        # Create frame for invoice details
        details_frame = tk.Frame(history_frame, bg="#f0f0f0", pady=10)
        details_frame.pack(fill="x")
        
        # Label for invoice details
        tk.Label(details_frame, text="Invoice Details:", font=self.header_font, bg="#f0f0f0").pack(anchor="w")
        
        # Text widget for invoice details
        self.invoice_details_text = tk.Text(details_frame, height=10, width=70, font=self.normal_font)
        self.invoice_details_text.pack(fill="both", expand=True, pady=5)
    
            
    def show_customer_info_dialog(self):
        """Show dialog to add customer info from bill tab"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Customer Info")
        dialog.geometry("450x300")
        dialog.configure(bg="#f0f0f0")
        dialog.transient(self.root)
        dialog.grab_set()

        # Customer frame
        customer_frame = tk.Frame(dialog, bg="#f0f0f0", padx=20, pady=20)
        customer_frame.pack(fill=tk.BOTH, expand=True)

        # Customer name
        name_frame = tk.Frame(customer_frame, bg="#f0f0f0")
        name_frame.pack(fill="x", pady=5)

        tk.Label(name_frame, text="Customer Name:", font=self.normal_font, bg="#f0f0f0", width=15, anchor="w").pack(side="left")
        bill_customer_name_var = tk.StringVar()
        name_combobox = ttk.Combobox(name_frame, textvariable=bill_customer_name_var, font=self.normal_font, width=23)
        name_combobox.pack(side="left", padx=5)
        name_combobox.bind('<KeyRelease>', lambda e: self.update_name_suggestions(name_combobox))

        # Customer mobile
        mobile_frame = tk.Frame(customer_frame, bg="#f0f0f0")
        mobile_frame.pack(fill="x", pady=5)

        tk.Label(mobile_frame, text="Mobile Number:", font=self.normal_font, bg="#f0f0f0", width=15, anchor="w").pack(side="left")
        bill_customer_mobile_var = tk.StringVar()
        mobile_combobox = ttk.Combobox(mobile_frame, textvariable=bill_customer_mobile_var, font=self.normal_font, width=23)
        mobile_combobox.pack(side="left", padx=5)
        mobile_combobox.bind('<KeyRelease>', lambda e: self.update_mobile_suggestions(mobile_combobox))

        # Customer DOB
        dob_frame = tk.Frame(customer_frame, bg="#f0f0f0")
        dob_frame.pack(fill="x", pady=5)

        tk.Label(dob_frame, text="Date of Birth:\n(DD/MM/YYYY)", font=self.normal_font, bg="#f0f0f0", width=15, anchor="w").pack(side="left")
        bill_customer_dob_var = tk.StringVar()
        tk.Entry(dob_frame, textvariable=bill_customer_dob_var, font=self.normal_font, width=25).pack(side="left", padx=5)

        # Customer Email
        email_frame = tk.Frame(customer_frame, bg="#f0f0f0")
        email_frame.pack(fill="x", pady=5)

        tk.Label(email_frame, text="Email (optional):", font=self.normal_font, bg="#f0f0f0", width=15, anchor="w").pack(side="left")
        bill_customer_email_var = tk.StringVar()
        tk.Entry(email_frame, textvariable=bill_customer_email_var, font=self.normal_font, width=25).pack(side="left", padx=5)

        # Status message
        bill_customer_status_var = tk.StringVar()
        status_label = tk.Label(customer_frame, textvariable=bill_customer_status_var, font=self.normal_font, bg="#f0f0f0", fg="#F44336")
        status_label.pack(pady=10)

        # Save button
        save_button = tk.Button(
            customer_frame,
            text="Add to Bill",
            command=lambda: self.controller.save_customer_info_from_bill(
                bill_customer_name_var.get(),
                bill_customer_mobile_var.get(),
                bill_customer_dob_var.get(),
                bill_customer_email_var.get(),
                bill_customer_status_var,
                dialog
            ),
            font=self.normal_font,
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5
        )
        save_button.pack(pady=20)
    
    def show_invoice_history_dialog(self):
        """Show dialog to view invoice history by mobile number"""
        dialog = tk.Toplevel(self.root)
        dialog.title("View Invoice History")
        dialog.geometry("500x400")
        dialog.configure(bg="#f0f0f0")
        dialog.transient(self.root)
        dialog.grab_set()

        # Main frame
        main_frame = tk.Frame(dialog, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Mobile input frame
        mobile_frame = tk.Frame(main_frame, bg="#f0f0f0")
        mobile_frame.pack(fill="x", pady=(0, 10))

        tk.Label(mobile_frame, text="Mobile Number:", font=self.normal_font, bg="#f0f0f0").pack(side="left")
        mobile_var = tk.StringVar()
        mobile_entry = tk.Entry(mobile_frame, textvariable=mobile_var, font=self.normal_font, width=20)
        mobile_entry.pack(side="left", padx=10)

        # Search button
        search_button = tk.Button(
            mobile_frame,
            text="Search",
            command=lambda: self.controller.search_invoice_history(mobile_var.get(), history_text),
            font=self.normal_font,
            bg="#2196F3",
            fg="white",
            padx=15,
            pady=2
        )
        search_button.pack(side="left", padx=10)

        # History display
        history_frame = tk.Frame(main_frame, bg="#f0f0f0")
        history_frame.pack(fill="both", expand=True)

        history_text = tk.Text(history_frame, font=self.normal_font, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(history_frame, orient="vertical", command=history_text.yview)
        history_text.configure(yscrollcommand=scrollbar.set)

        history_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Initial message
        history_text.insert(tk.END, "Enter a mobile number and click Search to view invoice history.")
        history_text.config(state=tk.DISABLED)
    
    
    def setup_employee_tab(self):
        """Setup the employee panel tab"""
        # Create frame for employee panel
        employee_frame = tk.Frame(self.employee_tab, bg="#f0f0f0", padx=20, pady=20)
        employee_frame.pack(fill=tk.BOTH, expand=True)
        
        # Welcome message
        welcome_label = tk.Label(
            employee_frame,
            text="Master Employee Panel",
            font=self.header_font,
            bg="#f0f0f0",
            fg="#333333"
        )
        welcome_label.pack(pady=(0, 20))
        
        # Create notebook for employee functions
        employee_notebook = ttk.Notebook(employee_frame)
        employee_notebook.pack(fill="both", expand=True)
        
        # Create tabs
        sales_report_tab = tk.Frame(employee_notebook, bg="#f0f0f0")
        customer_management_tab = tk.Frame(employee_notebook, bg="#f0f0f0")
        
        # Add tabs to notebook
        employee_notebook.add(sales_report_tab, text="Sales Reports")
        employee_notebook.add(customer_management_tab, text="Customer Management")
        
        # Setup sales report tab
        self.setup_sales_report_tab(sales_report_tab)
        
        # Setup customer management tab
        self.setup_customer_management_tab(customer_management_tab)
        
        # Email configuration button
        email_config_button = tk.Button(
            employee_frame,
            text="Configure Email",
            command=self.show_email_config_dialog,
            font=self.normal_font,
            bg="#FF9800",
            fg="white",
            padx=10,
            pady=5
        )
        email_config_button.pack(pady=5)
        
    
    def setup_sales_report_tab(self, parent_frame):
        """Setup the sales report tab"""
        # Create frame for sales report
        report_frame = tk.Frame(parent_frame, bg="#f0f0f0", padx=10, pady=10)
        report_frame.pack(fill="both", expand=True)
        
        # Date range selection
        date_frame = tk.Frame(report_frame, bg="#f0f0f0")
        date_frame.pack(fill="x", pady=10)
        
        # From date
        tk.Label(date_frame, text="From Date (DD/MM/YYYY):", font=self.normal_font, bg="#f0f0f0").pack(side="left", padx=5)
        self.from_date_var = tk.StringVar()
        tk.Entry(date_frame, textvariable=self.from_date_var, font=self.normal_font, width=12).pack(side="left", padx=5)
        
        # To date
        tk.Label(date_frame, text="To Date (DD/MM/YYYY):", font=self.normal_font, bg="#f0f0f0").pack(side="left", padx=5)
        self.to_date_var = tk.StringVar()
        tk.Entry(date_frame, textvariable=self.to_date_var, font=self.normal_font, width=12).pack(side="left", padx=5)
        
        # Set default dates (last 7 days)
        today = datetime.now()
        week_ago = today - timedelta(days=7)
        self.from_date_var.set(week_ago.strftime("%d/%m/%Y"))
        self.to_date_var.set(today.strftime("%d/%m/%Y"))
        
        # Generate report button
        generate_button = tk.Button(
            date_frame,
            text="Generate Report",
            command=self.controller.generate_sales_report,
            font=self.normal_font,
            bg="#2196F3",
            fg="white",
            padx=10,
            pady=2
        )
        generate_button.pack(side="left", padx=10)
        
        # Report text
        self.report_text = tk.Text(report_frame, height=20, width=70, font=self.normal_font)
        self.report_text.pack(fill="both", expand=True, pady=10)
    
    def setup_customer_management_tab(self, parent_frame):
        """Setup the customer management tab"""
        # Create frame for customer management
        customer_frame = tk.Frame(parent_frame, bg="#f0f0f0", padx=10, pady=10)
        customer_frame.pack(fill="both", expand=True)
        
        # Search frame
        search_frame = tk.Frame(customer_frame, bg="#f0f0f0")
        search_frame.pack(fill="x", pady=10)
        
        # Search by mobile
        tk.Label(search_frame, text="Search by Mobile:", font=self.normal_font, bg="#f0f0f0").pack(side="left", padx=5)
        self.customer_search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.customer_search_var, font=self.normal_font, width=15).pack(side="left", padx=5)
        
        # Search button
        search_button = tk.Button(
            search_frame,
            text="Search",
            command=self.controller.search_customers,
            font=self.normal_font,
            bg="#2196F3",
            fg="white",
            padx=10,
            pady=2
        )
        search_button.pack(side="left", padx=10)
        
        # Create treeview for customers
        columns = ("ID", "Name", "Mobile", "DOB", "Points", "Tier", "Registered Date")
        self.customer_tree = ttk.Treeview(customer_frame, columns=columns, show="headings", height=10)
        
        # Set column headings
        for col in columns:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=100, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(customer_frame, orient="vertical", command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.customer_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def update_cart_view(self, cart):
        """Update the cart view"""
        # Clear existing items
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Add items to treeview
        for item in cart:
            self.cart_tree.insert(
                "", "end", values=(
                    item['name'], 
                    item['quantity'], 
                    PriceFormatter.format_price(item['price']), 
                    PriceFormatter.format_price(item['total'])
                )
            )
    
    def update_bill_view(self, bill_text):
        """Update the bill view"""
        # Clear previous bill
        self.bill_text.delete(1.0, tk.END)
        
        # Insert new bill
        self.bill_text.insert(tk.END, bill_text)
    
    def update_invoice_view(self, invoices):
        """Update the invoice view"""
        # Clear existing items
        for item in self.invoice_tree.get_children():
            self.invoice_tree.delete(item)
        
        # Add invoices to treeview
        for invoice in invoices:
            self.invoice_tree.insert(
                "", "end", values=(
                    invoice['id'], 
                    invoice['date'], 
                    PriceFormatter.format_price(invoice['total']), 
                    PriceFormatter.format_price(invoice['discount']), 
                    PriceFormatter.format_price(invoice['final'])
                )
            )
    
    def update_invoice_details(self, invoice):
        """Update the invoice details view"""
        # Clear previous details
        self.invoice_details_text.delete(1.0, tk.END)
        
        # Format invoice details
        self.invoice_details_text.insert(tk.END, f"Invoice #{invoice['id']} - {invoice['date']}\n")
        self.invoice_details_text.insert(tk.END, f"Customer: {invoice['customer_name']} | Mobile: {invoice['mobile']}\n\n")
        
        self.invoice_details_text.insert(tk.END, f"{'Item':<20} {'Qty':<8} {'Price':<12} {'Total':<12}\n")
        self.invoice_details_text.insert(tk.END, "-" * 52 + "\n")
        
        for item in invoice['items']:
            self.invoice_details_text.insert(tk.END, f"{item['name']:<20} {item['quantity']:<8} {PriceFormatter.format_price(item['price']):<12} {PriceFormatter.format_price(item['total']):<12}\n")
        
        self.invoice_details_text.insert(tk.END, "-" * 52 + "\n")
        self.invoice_details_text.insert(tk.END, f"Subtotal: {PriceFormatter.format_price(invoice['total'])}\n")
        
        if invoice['discount'] > 0:
            self.invoice_details_text.insert(tk.END, f"Discount: {PriceFormatter.format_price(invoice['discount'])}\n")
        
        self.invoice_details_text.insert(tk.END, f"Final Amount: {PriceFormatter.format_price(invoice['final'])}\n")
    
    def update_customer_tree(self, customers):
        """Update the customer tree view"""
        # Clear existing items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # Add customers to treeview
        for customer in customers:
            # Get reward tier
            tier = RewardSystem.get_reward_tier(customer['points'])
            
            self.customer_tree.insert(
                "", "end", values=(
                    customer['id'],
                    customer['name'],
                    customer['mobile'],
                    customer['dob'],
                    customer['points'],
                    tier,
                    customer['created_at']
                )
            )
    
    def update_sales_report(self, report_data, from_date, to_date):
        """Update the sales report view"""
        # Clear previous report
        self.report_text.delete(1.0, tk.END)
        
        # Format report
        self.report_text.insert(tk.END, f"Sales Report: {from_date} to {to_date}\n")
        self.report_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # Sales summary
        if report_data['invoice_count'] == 0:
            self.report_text.insert(tk.END, "No sales data for the selected period.\n")
            return
            
        self.report_text.insert(tk.END, f"Total Invoices: {report_data['invoice_count']}\n")
        self.report_text.insert(tk.END, f"Total Sales: {PriceFormatter.format_price(report_data['total_sales'])}\n")
        self.report_text.insert(tk.END, f"Total Discounts: {PriceFormatter.format_price(report_data['total_discount'])}\n")
        self.report_text.insert(tk.END, f"Net Sales: {PriceFormatter.format_price(report_data['final_sales'])}\n\n")
        
        # Top selling items
        self.report_text.insert(tk.END, "Top Selling Items:\n")
        self.report_text.insert(tk.END, "-" * 50 + "\n")
        self.report_text.insert(tk.END, f"{'Item':<30} {'Quantity':<10} {'Sales':<10}\n")
        self.report_text.insert(tk.END, "-" * 50 + "\n")
        
        for item in report_data['top_items']:
            self.report_text.insert(tk.END, f"{item['name']:<30} {item['quantity']:<10} {PriceFormatter.format_price(item['sales']):<10}\n")
    
    def show_message(self, title, message, error=False):
        """Show a message dialog"""
        if error:
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)
    
    def ask_confirmation(self, title, message):
        """Show a confirmation dialog and return True if user confirms"""
        return messagebox.askyesno(title, message)

    def update_name_suggestions(self, combobox):
        """Update name suggestions for autocomplete"""
        current_text = combobox.get()
        if len(current_text) >= 2:  # Start suggesting after 2 characters
            suggestions = self.controller.get_customer_name_suggestions(current_text)
            combobox['values'] = suggestions
        else:
            combobox['values'] = []

    def update_mobile_suggestions(self, combobox):
        """Update mobile suggestions for autocomplete"""
        current_text = combobox.get()
        if len(current_text) >= 3:  # Start suggesting after 3 characters
            suggestions = self.controller.get_customer_mobile_suggestions(current_text)
            combobox['values'] = suggestions
        else:
            combobox['values'] = []