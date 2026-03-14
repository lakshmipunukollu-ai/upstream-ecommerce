from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category, Product
from accounts.models import User


class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Categories
        categories_data = [
            {'name': 'Phonics', 'description': 'Phonics and phonemic awareness materials'},
            {'name': 'Reading Comprehension', 'description': 'Reading comprehension curricula'},
            {'name': 'Writing', 'description': 'Writing instruction materials'},
            {'name': 'Vocabulary', 'description': 'Vocabulary building resources'},
            {'name': 'ELL/Bilingual', 'description': 'English Language Learner materials'},
            {'name': 'Intervention', 'description': 'Reading intervention programs'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=slugify(cat_data['name']),
                defaults=cat_data
            )
            categories[cat.name] = cat

        # Products
        products_data = [
            {
                'title': 'Foundations of Phonics K-2',
                'description': 'A comprehensive phonics program for Kindergarten through 2nd grade. Includes decodable readers, letter-sound cards, and teacher guides. Research-based approach following the science of reading.',
                'price': '249.99',
                'stock': 150,
                'category': categories['Phonics'],
                'grade_levels': ['K', '1', '2'],
                'images': ['/images/phonics-k2.jpg'],
            },
            {
                'title': 'Advanced Phonics 3-5',
                'description': 'Advanced phonics and word study for grades 3-5. Covers multisyllabic words, morphology, and etymology. Perfect for building decoding skills in upper elementary.',
                'price': '199.99',
                'stock': 100,
                'category': categories['Phonics'],
                'grade_levels': ['3', '4', '5'],
                'images': ['/images/phonics-35.jpg'],
            },
            {
                'title': 'Comprehension Toolkit Grade 3-5',
                'description': 'Interactive reading comprehension strategies for grades 3-5. Teaches summarizing, inferring, questioning, and synthesizing with authentic texts.',
                'price': '179.99',
                'stock': 200,
                'category': categories['Reading Comprehension'],
                'grade_levels': ['3', '4', '5'],
                'images': ['/images/comp-35.jpg'],
            },
            {
                'title': 'Early Readers Comprehension K-2',
                'description': 'Age-appropriate comprehension activities for early readers. Uses picture books and leveled texts to build understanding.',
                'price': '149.99',
                'stock': 175,
                'category': categories['Reading Comprehension'],
                'grade_levels': ['K', '1', '2'],
                'images': ['/images/comp-k2.jpg'],
            },
            {
                'title': 'Writers Workshop Complete Kit',
                'description': 'Full writing workshop curriculum for grades 2-5. Includes narrative, informational, and opinion writing units with mentor texts and mini-lessons.',
                'price': '299.99',
                'stock': 80,
                'category': categories['Writing'],
                'grade_levels': ['2', '3', '4', '5'],
                'images': ['/images/writing-25.jpg'],
            },
            {
                'title': 'Vocabulary Power Grades 3-8',
                'description': 'Research-based vocabulary instruction program. Teaches word-learning strategies, context clues, and academic vocabulary across content areas.',
                'price': '129.99',
                'stock': 250,
                'category': categories['Vocabulary'],
                'grade_levels': ['3', '4', '5', '6', '7', '8'],
                'images': ['/images/vocab-38.jpg'],
            },
            {
                'title': 'Puente Bilingual Literacy Program',
                'description': 'Comprehensive bilingual literacy program (Spanish/English). Designed for dual-language and transitional bilingual classrooms. Aligned with WIDA standards.',
                'price': '349.99',
                'stock': 60,
                'category': categories['ELL/Bilingual'],
                'grade_levels': ['K', '1', '2', '3'],
                'images': ['/images/bilingual-k3.jpg'],
            },
            {
                'title': 'ELL Newcomer Kit',
                'description': 'Essential materials for English Language Learner newcomers. Visual vocabulary cards, simplified texts, and language development activities.',
                'price': '199.99',
                'stock': 120,
                'category': categories['ELL/Bilingual'],
                'grade_levels': ['K', '1', '2', '3', '4', '5'],
                'images': ['/images/ell-newcomer.jpg'],
            },
            {
                'title': 'Reading Recovery Intervention Level 1',
                'description': 'Intensive one-on-one reading intervention for struggling first graders. Based on Marie Clay\'s Reading Recovery model with running records and leveled books.',
                'price': '399.99',
                'stock': 45,
                'category': categories['Intervention'],
                'grade_levels': ['1'],
                'images': ['/images/intervention-1.jpg'],
            },
            {
                'title': 'Literacy Intervention Grades 3-5',
                'description': 'Small-group intervention program for students reading below grade level. Systematic instruction in fluency, comprehension, and word study.',
                'price': '279.99',
                'stock': 90,
                'category': categories['Intervention'],
                'grade_levels': ['3', '4', '5'],
                'images': ['/images/intervention-35.jpg'],
            },
        ]

        for prod_data in products_data:
            Product.objects.get_or_create(
                slug=slugify(prod_data['title']),
                defaults=prod_data,
            )

        # Create admin user
        if not User.objects.filter(email='admin@upstream.edu').exists():
            User.objects.create_superuser(
                email='admin@upstream.edu',
                password='admin123',
                first_name='Admin',
                last_name='User',
            )

        # Create test user
        if not User.objects.filter(email='teacher@school.edu').exists():
            user = User.objects.create_user(
                email='teacher@school.edu',
                password='teacher123',
                first_name='Jane',
                last_name='Smith',
            )
            from accounts.models import DistrictProfile
            DistrictProfile.objects.create(
                user=user,
                district_name='Springfield School District',
                state='IL',
                student_count=5000,
                ell_percentage=25.0,
                free_reduced_lunch_pct=45.0,
                grade_levels_served=['K', '1', '2', '3', '4', '5'],
            )

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {Category.objects.count()} categories and {Product.objects.count()} products'
        ))
