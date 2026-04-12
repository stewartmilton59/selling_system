from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from sales.models import Category, Product, Customer
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Creates sample data for the selling system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create categories
        categories_data = [
            {'name': 'Electronics', 'slug': 'electronics', 'description': 'Latest electronic gadgets and devices'},
            {'name': 'Fashion', 'slug': 'fashion', 'description': 'Trendy clothing and accessories'},
            {'name': 'Home & Living', 'slug': 'home-living', 'description': 'Home decor and furniture'},
            {'name': 'Sports', 'slug': 'sports', 'description': 'Sports equipment and accessories'},
            {'name': 'Books', 'slug': 'books', 'description': 'Books and educational materials'},
            {'name': 'Beauty', 'slug': 'beauty', 'description': 'Beauty and personal care products'},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products
        products_data = [
            # Electronics
            {'name': 'Wireless Bluetooth Headphones', 'slug': 'wireless-bluetooth-headphones', 'description': 'High-quality wireless headphones with noise cancellation and 20-hour battery life.', 'price': Decimal('79.99'), 'stock': 50, 'category': categories[0], 'is_featured': True},
            {'name': 'Smart Watch Pro', 'slug': 'smart-watch-pro', 'description': 'Advanced smartwatch with health monitoring, GPS, and 7-day battery life.', 'price': Decimal('199.99'), 'stock': 30, 'category': categories[0], 'is_featured': True},
            {'name': 'Portable Power Bank 20000mAh', 'slug': 'portable-power-bank', 'description': 'High-capacity power bank with fast charging support for all devices.', 'price': Decimal('39.99'), 'stock': 100, 'category': categories[0]},
            {'name': 'Wireless Mouse', 'slug': 'wireless-mouse', 'description': 'Ergonomic wireless mouse with precision tracking and long battery life.', 'price': Decimal('24.99'), 'stock': 75, 'category': categories[0]},
            {'name': 'USB-C Hub', 'slug': 'usb-c-hub', 'description': 'Multi-port USB-C hub with HDMI, USB 3.0, and SD card reader.', 'price': Decimal('49.99'), 'stock': 40, 'category': categories[0]},
            
            # Fashion
            {'name': 'Classic Cotton T-Shirt', 'slug': 'classic-cotton-tshirt', 'description': 'Comfortable 100% cotton t-shirt available in multiple colors.', 'price': Decimal('19.99'), 'stock': 200, 'category': categories[1], 'is_featured': True},
            {'name': 'Denim Jeans', 'slug': 'denim-jeans', 'description': 'Premium quality denim jeans with perfect fit and comfort.', 'price': Decimal('59.99'), 'stock': 80, 'category': categories[1]},
            {'name': 'Leather Wallet', 'slug': 'leather-wallet', 'description': 'Genuine leather wallet with multiple card slots and coin pocket.', 'price': Decimal('34.99'), 'stock': 60, 'category': categories[1]},
            {'name': 'Sunglasses', 'slug': 'sunglasses', 'description': 'Stylish UV protection sunglasses with polarized lenses.', 'price': Decimal('29.99'), 'stock': 90, 'category': categories[1]},
            {'name': 'Running Shoes', 'slug': 'running-shoes', 'description': 'Lightweight running shoes with cushioned sole for maximum comfort.', 'price': Decimal('89.99'), 'stock': 45, 'category': categories[1], 'is_featured': True},
            
            # Home & Living
            {'name': 'LED Desk Lamp', 'slug': 'led-desk-lamp', 'description': 'Adjustable LED desk lamp with multiple brightness levels and color temperatures.', 'price': Decimal('44.99'), 'stock': 55, 'category': categories[2], 'is_featured': True},
            {'name': 'Coffee Maker', 'slug': 'coffee-maker', 'description': 'Programmable coffee maker with thermal carafe and auto-brew feature.', 'price': Decimal('79.99'), 'stock': 25, 'category': categories[2]},
            {'name': 'Throw Pillows Set', 'slug': 'throw-pillows-set', 'description': 'Set of 4 decorative throw pillows with removable covers.', 'price': Decimal('34.99'), 'stock': 70, 'category': categories[2]},
            {'name': 'Kitchen Knife Set', 'slug': 'kitchen-knife-set', 'description': 'Professional 6-piece kitchen knife set with wooden block.', 'price': Decimal('69.99'), 'stock': 35, 'category': categories[2]},
            {'name': 'Air Purifier', 'slug': 'air-purifier', 'description': 'HEPA air purifier for rooms up to 300 sq ft with quiet operation.', 'price': Decimal('129.99'), 'stock': 20, 'category': categories[2]},
            
            # Sports
            {'name': 'Yoga Mat', 'slug': 'yoga-mat', 'description': 'Non-slip yoga mat with carrying strap, perfect for all exercises.', 'price': Decimal('24.99'), 'stock': 100, 'category': categories[3], 'is_featured': True},
            {'name': 'Dumbbells Set', 'slug': 'dumbbells-set', 'description': 'Adjustable dumbbells set from 5 to 25 lbs for home workouts.', 'price': Decimal('99.99'), 'stock': 30, 'category': categories[3]},
            {'name': 'Resistance Bands', 'slug': 'resistance-bands', 'description': 'Set of 5 resistance bands with different strength levels.', 'price': Decimal('14.99'), 'stock': 150, 'category': categories[3]},
            {'name': 'Water Bottle', 'slug': 'water-bottle', 'description': 'Insulated stainless steel water bottle keeps drinks cold for 24 hours.', 'price': Decimal('19.99'), 'stock': 120, 'category': categories[3]},
            {'name': 'Foam Roller', 'slug': 'foam-roller', 'description': 'High-density foam roller for muscle recovery and massage.', 'price': Decimal('22.99'), 'stock': 65, 'category': categories[3]},
            
            # Books
            {'name': 'Python Programming Book', 'slug': 'python-programming-book', 'description': 'Comprehensive guide to Python programming for beginners and advanced users.', 'price': Decimal('39.99'), 'stock': 40, 'category': categories[4]},
            {'name': 'Business Strategy', 'slug': 'business-strategy', 'description': 'Essential guide to building successful business strategies.', 'price': Decimal('29.99'), 'stock': 50, 'category': categories[4]},
            {'name': 'Cookbook', 'slug': 'cookbook', 'description': 'Collection of 100+ delicious recipes from around the world.', 'price': Decimal('24.99'), 'stock': 60, 'category': categories[4]},
            {'name': 'Science Fiction Novel', 'slug': 'science-fiction-novel', 'description': 'Bestselling sci-fi novel that will keep you on the edge of your seat.', 'price': Decimal('14.99'), 'stock': 80, 'category': categories[4]},
            {'name': 'Self-Help Guide', 'slug': 'self-help-guide', 'description': 'Transform your life with practical tips and strategies.', 'price': Decimal('19.99'), 'stock': 70, 'category': categories[4]},
            
            # Beauty
            {'name': 'Face Moisturizer', 'slug': 'face-moisturizer', 'description': 'Hydrating face moisturizer for all skin types with SPF 30.', 'price': Decimal('29.99'), 'stock': 85, 'category': categories[5], 'is_featured': True},
            {'name': 'Hair Dryer', 'slug': 'hair-dryer', 'description': 'Professional ionic hair dryer with multiple heat settings.', 'price': Decimal('49.99'), 'stock': 40, 'category': categories[5]},
            {'name': 'Makeup Brush Set', 'slug': 'makeup-brush-set', 'description': 'Complete 10-piece makeup brush set with carrying case.', 'price': Decimal('34.99'), 'stock': 55, 'category': categories[5]},
            {'name': 'Shampoo & Conditioner', 'slug': 'shampoo-conditioner', 'description': 'Natural hair care set for healthy and shiny hair.', 'price': Decimal('24.99'), 'stock': 90, 'category': categories[5]},
            {'name': 'Perfume', 'slug': 'perfume', 'description': 'Elegant fragrance with long-lasting scent.', 'price': Decimal('59.99'), 'stock': 35, 'category': categories[5]},
        ]

        for prod_data in products_data:
            # Add discount to some products
            if random.random() < 0.3:  # 30% chance of discount
                discount = random.uniform(0.1, 0.3)
                prod_data['discount_price'] = prod_data['price'] * Decimal(1 - discount)
            
            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults=prod_data
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')

        # Create admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@prosell.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write('Created admin user (username: admin, password: admin123)')

        # Create sample customer
        if not User.objects.filter(username='customer').exists():
            user = User.objects.create_user(
                username='customer',
                email='customer@example.com',
                password='customer123',
                first_name='John',
                last_name='Doe'
            )
            customer = Customer.objects.get(user=user)
            customer.phone = '+1 555-123-4567'
            customer.address = '123 Main Street, Apt 4B'
            customer.city = 'New York'
            customer.state = 'NY'
            customer.zip_code = '10001'
            customer.save()
            self.stdout.write('Created sample customer (username: customer, password: customer123)')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
