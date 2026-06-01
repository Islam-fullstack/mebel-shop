from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Product, Review


CATEGORIES = [
    {'name': 'Divonlar',        'slug': 'divonlar',         'icon': '🛋️', 'description': 'Zamonaviy va klassik uslubdagi qulay divonlar'},
    {'name': 'Stol va Stullar', 'slug': 'stol-va-stullar',  'icon': '🪑', 'description': 'Osh xona, yozuv va ofis stol-stullari'},
    {'name': 'Yotoq xona',      'slug': 'yotoq-xona',       'icon': '🛏️', 'description': 'Karavotlar, matraslar va yotoq xona mebellar'},
    {'name': 'Shkaflar',        'slug': 'shkaflar',          'icon': '🗄️', 'description': 'Kiyim-kechak va kitob shkaflar'},
    {'name': 'Stol',            'slug': 'stollar',           'icon': '🪞', 'description': 'Ovqat va yozuv stollar'},
    {'name': 'Kreslolar',       'slug': 'kreslolar',         'icon': '💺', 'description': 'Dam olish va ofis kreslolari'},
]

PRODUCTS = [
    # Divonlar
    {
        'name': 'Milano Burchak Divan',
        'slug': 'milano-burchak-divan',
        'category': 'divonlar',
        'price': 8_500_000,
        'discount_price': 7_200_000,
        'description': 'Zamonaviy Milano uslubidagi burchak divan. Yotoq funksiyasi mavjud. Ichki yashirin o\'rin. Yumshoq premium mato bilan qoplangan. O\'lcham: 280x180 sm.',
        'material': 'mato',
        'color': 'Kulrang',
        'dimensions': '280x180x90 sm',
        'stock': 5,
        'is_featured': True,
    },
    {
        'name': 'Royal Klassik Divan',
        'slug': 'royal-klassik-divan',
        'category': 'divonlar',
        'price': 6_800_000,
        'discount_price': None,
        'description': 'Klassik Royal dizayndagi 3 o\'rinli divan. Baland sifatli dерево oyoqlar. Velvet mato. O\'lcham: 220x90 sm.',
        'material': 'mato',
        'color': 'To\'q ko\'k',
        'dimensions': '220x90x85 sm',
        'stock': 8,
        'is_featured': True,
    },
    {
        'name': 'Comfort Yotoq Divan',
        'slug': 'comfort-yotoq-divan',
        'category': 'divonlar',
        'price': 4_200_000,
        'discount_price': 3_800_000,
        'description': 'Kunlik yotoqqa aylanadigan qulay divan. Ortopedik matras. Ixcham o\'lcham kichik xonalar uchun ideal.',
        'material': 'mato',
        'color': 'Jigarrang',
        'dimensions': '190x85x80 sm',
        'stock': 12,
        'is_featured': False,
    },
    # Stol va Stullar
    {
        'name': 'Elegance Yozuv Stoli',
        'slug': 'elegance-yozuv-stoli',
        'category': 'stol-va-stullar',
        'price': 1_800_000,
        'discount_price': None,
        'description': 'Eman yog\'ochidan ishlangan zamonaviy yozuv stoli. Keng ish sathi. 3 ta tortma. Metal oyoqlar. Ofis va uy uchun.',
        'material': 'yogoch',
        'color': 'Yong\'oq',
        'dimensions': '140x70x76 sm',
        'stock': 15,
        'is_featured': True,
    },
    {
        'name': 'Ofis Aylanma Stul',
        'slug': 'ofis-aylanma-stul',
        'category': 'stol-va-stullar',
        'price': 980_000,
        'discount_price': 820_000,
        'description': 'Ergonomik dizayndagi ofis stuli. Balandligi rostlanadi. Bel suyanchiq. Yumshoq o\'tirgich. 5 g\'ildirakli asos.',
        'material': 'mato',
        'color': 'Qora',
        'dimensions': '65x65x90-105 sm',
        'stock': 20,
        'is_featured': False,
    },
    {
        'name': 'Osh Xona Stul To\'plami',
        'slug': 'osh-xona-stul-toplami',
        'category': 'stol-va-stullar',
        'price': 2_400_000,
        'discount_price': None,
        'description': '4 ta stuldan iborat to\'plam. Metall ramka, yumshoq o\'tirgich. Zamonaviy minimalist dizayn. Osh xona uchun ideal.',
        'material': 'aralash',
        'color': 'Oq/Kulrang',
        'dimensions': '45x50x90 sm (har biri)',
        'stock': 7,
        'is_featured': False,
    },
    # Yotoq xona
    {
        'name': 'Premium Karavot 160x200',
        'slug': 'premium-karavot-160x200',
        'category': 'yotoq-xona',
        'price': 4_500_000,
        'discount_price': 3_900_000,
        'description': 'Massiv yog\'ochdan ishlangan mustahkam karavot. O\'rnatilgan yotoq qutisi. Ortopedik tayanch. 160x200 matras uchun.',
        'material': 'yogoch',
        'color': 'Qarag\'ay',
        'dimensions': '170x210x100 sm',
        'stock': 6,
        'is_featured': True,
    },
    {
        'name': 'Modern Karavot 180x200',
        'slug': 'modern-karavot-180x200',
        'category': 'yotoq-xona',
        'price': 5_800_000,
        'discount_price': None,
        'description': 'Zamonaviy uslubdagi king size karavot. Bosh qismi yumshoq mato bilan qoplangan. LED yoritgich. 180x200 matras uchun.',
        'material': 'aralash',
        'color': 'Kulrang/Qora',
        'dimensions': '190x215x110 sm',
        'stock': 4,
        'is_featured': True,
    },
    # Shkaflar
    {
        'name': 'Klassik Kiyim Shkafi',
        'slug': 'klassik-kiyim-shkafi',
        'category': 'shkaflar',
        'price': 3_200_000,
        'discount_price': 2_800_000,
        'description': '3 eshikli keng kiyim shkafi. Ichida osilgich, javonlar va tortmalar. Oyna eshik. MDF dan ishlangan.',
        'material': 'yogoch',
        'color': 'Oq',
        'dimensions': '180x60x220 sm',
        'stock': 9,
        'is_featured': False,
    },
    {
        'name': 'Yotoq Xona Garderob',
        'slug': 'yotoq-xona-garderob',
        'category': 'shkaflar',
        'price': 5_500_000,
        'discount_price': None,
        'description': 'Keng garderob shkaf. Siljuvchi eshiklar. Ichki yoritgich. Har xil bo\'limlar. Buyurtma bo\'yicha ranglar.',
        'material': 'yogoch',
        'color': 'Yong\'oq/Oq',
        'dimensions': '240x65x240 sm',
        'stock': 3,
        'is_featured': True,
    },
    # Kreslolar
    {
        'name': 'Barcelona Kreslo',
        'slug': 'barcelona-kreslo',
        'category': 'kreslolar',
        'price': 2_100_000,
        'discount_price': 1_850_000,
        'description': 'Zamonaviy Barcelona uslubidagi kreslo. Yumshoq to\'ldirilgan o\'tirgich. Metall oyoqlar. Dam olish va mehmonxona uchun.',
        'material': 'teri',
        'color': 'Qora',
        'dimensions': '80x80x75 sm',
        'stock': 10,
        'is_featured': True,
    },
    {
        'name': 'Yumshoq Dam Olish Kreslo',
        'slug': 'yumshoq-dam-olish-kreslo',
        'category': 'kreslolar',
        'price': 1_600_000,
        'discount_price': None,
        'description': 'Qulay dam olish kreslosi. Orqa yastiq birga. Yon stolcha mavjud. Kitob o\'qish va TV ko\'rish uchun ideal.',
        'material': 'mato',
        'color': 'Kremrang',
        'dimensions': '85x90x100 sm',
        'stock': 14,
        'is_featured': False,
    },
]

REVIEWS_DATA = [
    (5, "Juda ajoyib mahsulot! Sifati yuqori, yetkazib berish tez bo'ldi. Albatta yana buyurtma beraman."),
    (4, "Yaxshi mahsulot, kutganimdan ham chiroyli chiqdi. Faqat o'rnatish biroz qiyin bo'ldi."),
    (5, "Narx/sifat nisbati a'lo darajada. Do'stlarimga ham tavsiya qilaman."),
    (4, "Dizayni juda yoqdi. Material sifati yuqori. Xizmat ham yaxshi."),
    (3, "O'rtacha mahsulot. Rasmda ko'ringandan biroz kichikroq. Lekin sifati yaxshi."),
    (5, "Juda mamnun qoldim! Uyimizga juda mos tushdi. Rahmat!"),
]


class Command(BaseCommand):
    help = 'Seed database with default categories, products and reviews'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # Categories
        cat_map = {}
        for data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=data['slug'],
                defaults={'name': data['name'], 'icon': data['icon'], 'description': data['description']}
            )
            cat_map[data['slug']] = cat
            if created:
                self.stdout.write(f"  ✓ Category: {data['name']}")

        # Demo users for reviews
        demo_users = []
        for i, (uname, fname) in enumerate([
            ('akbar_uz', 'Akbar'), ('malika_t', 'Malika'),
            ('jasur99', 'Jasur'), ('nilufar_m', 'Nilufar'),
        ]):
            u, created = User.objects.get_or_create(
                username=uname,
                defaults={'first_name': fname, 'email': f'{uname}@demo.uz', 'password': 'demo'}
            )
            demo_users.append(u)

        # Products + Reviews
        for i, data in enumerate(PRODUCTS):
            cat = cat_map.get(data['category'])
            if not cat:
                continue
            product, created = Product.objects.get_or_create(
                slug=data['slug'],
                defaults={
                    'name': data['name'],
                    'category': cat,
                    'price': data['price'],
                    'discount_price': data.get('discount_price'),
                    'description': data['description'],
                    'material': data['material'],
                    'color': data['color'],
                    'dimensions': data['dimensions'],
                    'stock': data['stock'],
                    'is_featured': data['is_featured'],
                    'is_available': True,
                }
            )
            if created:
                self.stdout.write(f"  ✓ Product: {data['name']}")
                # Add 2 reviews per product
                for j, user in enumerate(demo_users[:2]):
                    rating, comment = REVIEWS_DATA[(i + j) % len(REVIEWS_DATA)]
                    Review.objects.get_or_create(
                        product=product, user=user,
                        defaults={'rating': rating, 'comment': comment}
                    )

        self.stdout.write(self.style.SUCCESS('\nSeeding complete!'))
        self.stdout.write(f"  Categories: {Category.objects.count()}")
        self.stdout.write(f"  Products:   {Product.objects.count()}")
        self.stdout.write(f"  Reviews:    {Review.objects.count()}")