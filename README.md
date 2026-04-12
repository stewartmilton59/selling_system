# ProSell - Professional Selling System

A comprehensive Django-based e-commerce platform built with HTML, CSS, Bootstrap, and JavaScript.

## Features

### Customer Features
- **Product Catalog**: Browse products by categories with search and filter options
- **Shopping Cart**: Add/remove items, update quantities, view cart summary
- **User Authentication**: Register, login, logout, password reset
- **User Profile**: Manage personal information and view order history
- **Wishlist**: Save favorite products for later
- **Checkout**: Secure checkout process with multiple payment options
- **Order Tracking**: Track order status and view order details

### Admin Features
- **Dashboard**: Sales analytics and statistics
- **Product Management**: Add, edit, delete products and categories
- **Order Management**: View and update order status
- **Customer Management**: View customer information and orders
- **Review Management**: Manage product reviews

## Tech Stack

- **Backend**: Django 5.x
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite (default), can be configured for PostgreSQL/MySQL
- **Icons**: Bootstrap Icons
- **Fonts**: Google Fonts (Poppins)

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd selling_system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create sample data (optional)**
   ```bash
   python manage.py create_sample_data
   ```

5. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Website: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Default Login Credentials

### Admin User
- **Username**: admin
- **Password**: admin123

### Sample Customer
- **Username**: customer
- **Password**: customer123

## Project Structure

```
selling_system/
├── selling_system/          # Main project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── sales/                   # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Form classes
│   ├── urls.py              # App URL patterns
│   ├── admin.py             # Admin configuration
│   ├── cart.py              # Shopping cart functionality
│   └── templates/           # HTML templates
├── templates/               # Base templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User-uploaded files
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Key Models

- **Category**: Product categories
- **Product**: Product information with stock management
- **Customer**: Extended user profile
- **Order**: Order information and status
- **OrderItem**: Individual items in an order
- **Review**: Product reviews and ratings
- **Wishlist**: User's saved products

## Features in Detail

### Shopping Cart
- Session-based cart storage
- Add/remove/update items
- Quantity validation against stock
- Cart summary with totals

### Checkout Process
- Shipping information collection
- Multiple payment methods (COD, Card, PayPal)
- Automatic tax and shipping calculation
- Order confirmation

### Admin Dashboard
- Sales statistics
- Order status tracking
- Top selling products
- Recent orders
- Quick action buttons

### Responsive Design
- Mobile-first approach
- Bootstrap 5 grid system
- Touch-friendly interface
- Optimized for all screen sizes

## Customization

### Changing Colors
Edit `static/css/style.css` to modify the color scheme:
```css
:root {
    --bs-primary: #your-color;
    --bs-secondary: #your-color;
}
```

### Adding New Categories
1. Login to admin panel
2. Navigate to Sales > Categories
3. Click "Add Category"

### Adding New Products
1. Login to admin panel
2. Navigate to Sales > Products
3. Click "Add Product"

## Security Features

- CSRF protection
- Password hashing
- Session security
- XSS protection
- SQL injection prevention

## Performance Optimizations

- Static file compression
- Database query optimization
- Lazy loading images
- Efficient pagination

## License

This project is open-source and available for personal and commercial use.

## Support

For support or questions, please contact: support@prosell.com

---

Built with ❤️ using Django and Bootstrap
