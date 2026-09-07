from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category, Product

DATA = {
    "Mobiles": [
        ("Pixel Nova 12 Pro (256GB)", 74999, 61999, "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600"),
        ("Galaxy Orbit S24", 59999, 49999, "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=600"),
        ("iSpark 15", 79900, None, "https://images.unsplash.com/photo-1592286927505-1def25115558?w=600"),
    ],
    "Laptops": [
        ("AeroBook Air 14\"", 84999, 72999, "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600"),
        ("ThinkForce Pro 15", 65999, 57999, "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600"),
        ("GameX Titan RTX", 129999, 109999, "https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?w=600"),
    ],
    "Fashion": [
        ("Men's Slim Fit Casual Shirt", 1499, 799, "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=600"),
        ("Women's Ethnic Kurti Set", 2199, 1299, "https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=600"),
        ("Running Sneakers Pro", 3999, 2499, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600"),
    ],
    "Home & Kitchen": [
        ("Non-stick Cookware Set (5 pcs)", 3499, 2199, "https://images.unsplash.com/photo-1584990347449-a0d8d8f0e5f2?w=600"),
        ("Smart LED Desk Lamp", 1299, 899, "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600"),
        ("Memory Foam Pillow (Set of 2)", 1799, None, "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=600"),
    ],
    "Electronics & Accessories": [
        ("Wireless Noise Cancelling Headphones", 6999, 4499, "https://images.unsplash.com/photo-1518444065439-e933c06ce9cd?w=600"),
        ("SmartWatch Fit 3", 4999, 3299, "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600"),
        ("65W Fast Charging Power Bank", 1999, 1299, "https://images.unsplash.com/photo-1609592424959-89c7ea3ffa79?w=600"),
    ],
}


class Command(BaseCommand):
    help = "Seed sample categories and products for Shopingly X"

    def handle(self, *args, **options):
        created_products = 0
        for cat_name, products in DATA.items():
            category, _ = Category.objects.get_or_create(
                name=cat_name, defaults={"slug": slugify(cat_name)}
            )
            for name, price, offer_price, image_url in products:
                slug = slugify(name)
                if Product.objects.filter(slug=slug).exists():
                    continue
                Product.objects.create(
                    category=category,
                    name=name,
                    slug=slug,
                    description=f"{name} — a great pick from our {cat_name} range, "
                                 f"backed by Shopingly X quality assurance and easy returns.",
                    image_url=image_url,
                    price=price,
                    offer_price=offer_price,
                    stock=25,
                    rating=4.2,
                )
                created_products += 1
        self.stdout.write(self.style.SUCCESS(
            f"Seeded {created_products} products across {len(DATA)} categories."
        ))
