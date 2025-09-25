# utils.py - Utility functions for the shopping cart application

import re
from datetime import datetime

class Validator:
    @staticmethod
    def validate_name(name):
        """Validate customer name"""
        if not name or len(name.strip()) < 3:
            return False, "Name must be at least 3 characters long"
        return True, ""
    
    @staticmethod
    def validate_mobile(mobile):
        """Validate mobile number (10 digits)"""
        if not mobile or not re.match(r'^\d{10}$', mobile):
            return False, "Mobile number must be 10 digits"
        return True, ""
    
    @staticmethod
    def validate_date(date_str):
        """Validate date in DD/MM/YYYY format"""
        if not date_str:
            return True, ""  # Date is optional
            
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True, ""
        except ValueError:
            return False, "Date must be in DD/MM/YYYY format"
    
    @staticmethod
    def validate_email(email):
        """Validate email address"""
        if not email:
            return True, ""  # Email is optional
            
        # Simple email validation pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        return True, ""


class RewardSystem:
    @staticmethod
    def calculate_points(amount):
        """Calculate reward points (10 points per ₹100)"""
        return int(amount / 100) * 10
    
    @staticmethod
    def get_reward_tier(points):
        """Get reward tier based on points"""
        if points >= 1000:
            return "Gold"
        elif points >= 500:
            return "Silver"
        else:
            return "Bronze"
    
    @staticmethod
    def get_discount_percentage(tier):
        """Get discount percentage based on tier"""
        if tier == "Gold":
            return 0.15  # 15% discount
        elif tier == "Silver":
            return 0.10  # 10% discount
        else:
            return 0.05  # 5% discount


class PriceFormatter:
    @staticmethod
    def format_price(price):
        """Format price with rupee symbol"""
        return f"₹{price:.2f}"
    
    @staticmethod
    def format_bill(cart, subtotal, discount=0, final=None, customer_name=None, customer_mobile=None, reward_tier=None):
        """Format bill details"""
        bill = "\n" + "=" * 50 + "\n"
        bill += "SHOPPING CART BILL\n"
        bill += "=" * 50 + "\n\n"
        
        # Add customer information if provided
        if customer_name and customer_mobile:
            bill += f"Customer: {customer_name}\n"
            bill += f"Mobile: {customer_mobile}\n"
            if reward_tier:
                bill += f"Reward Tier: {reward_tier}\n"
            bill += "\n"
        
        bill += f"{'Item':<30} {'Qty':<8} {'Price':<12} {'Total':<12}\n"
        bill += "-" * 62 + "\n"
        
        for item in cart:
            bill += f"{item['name']:<30} {item['quantity']:<8} {PriceFormatter.format_price(item['price']):<12} {PriceFormatter.format_price(item['total']):<12}\n"
        
        bill += "-" * 62 + "\n"
        bill += f"Subtotal: {PriceFormatter.format_price(subtotal)}\n"
        
        if discount > 0:
            bill += f"Discount: {PriceFormatter.format_price(discount)}\n"
            
        if final is not None:
            bill += f"Final Amount: {PriceFormatter.format_price(final)}\n"
        
        return bill