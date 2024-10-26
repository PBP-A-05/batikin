from django.core.management.base import BaseCommand
import json
from pathlib import Path
from shopping.models import Product

class Command(BaseCommand):
    help = 'Load products from JSON files into database'

    def determine_category(self, product_name, file_type):
        """Helper function to determine category based on product name and file type"""
        product_name_lower = product_name.lower()
        
        # Override based on file type
        if file_type == 'kain_batik':
            return 'aksesoris'
        elif file_type == 'pakaian_batik_laki':
            return 'pakaian_pria'
        elif file_type == 'pakaian_batik_perempuan':
            return 'pakaian_wanita'
        elif file_type == 'sesuatu_jogja':
            return 'aksesoris'
            
        # Fallback logic if needed
        if 'wanita' in product_name_lower:
            return 'pakaian_wanita'
        elif 'pria' in product_name_lower:
            return 'pakaian_pria'
        elif any(word in product_name_lower for word in ['gelang', 'kalung', 'cincin', 'kain']):
            return 'aksesoris'
        elif 'workshop' in product_name_lower:
            return 'workshop'
        
        return 'pakaian_pria'  # Default category

    def load_json_file(self, file_path, file_type):
        """Helper function to load and process a single JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                products_data = json.load(f)

            products_to_create = []
            for item in products_data:
                try:
                    product = Product(
                        store_url=item['Store URL'],
                        store_address=item['Store Address'],
                        product_name=item['Product Name'],
                        price=item['Price'],
                        image_urls=item['Image URLs'],
                        additional_info=item.get('Additional Info', ''),
                        product_link=item['Product Link'],
                        category=self.determine_category(item['Product Name'], file_type)
                    )
                    products_to_create.append(product)
                except KeyError as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Skipping product due to missing field: {e} in {file_path}'
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Error processing product in {file_path}: {str(e)}'
                        )
                    )
            
            return products_to_create
            
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(
                    f'Could not find JSON file at {file_path}'
                )
            )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(
                    f'Invalid JSON file: {file_path}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'An error occurred while processing {file_path}: {str(e)}'
                )
            )
        return []

    def handle(self, *args, **kwargs):
        # Clear existing products
        self.stdout.write('Deleting existing products...')
        Product.objects.all().delete()
        
        # Define JSON files to process
        json_files = [
            ('static/assets/kain_batik.json', 'kain_batik'),
            ('static/assets/pakaian_batik_laki.json', 'pakaian_batik_laki'),
            ('static/assets/pakaian_batik_perempuan.json', 'pakaian_batik_perempuan'),
            ('static/assets/sesuatu_jogja.json', 'sesuatu_jogja')
        ]
        
        all_products = []
        
        # Process each JSON file
        for file_path, file_type in json_files:
            self.stdout.write(f'Loading JSON from {file_path}...')
            products = self.load_json_file(Path(file_path), file_type)
            all_products.extend(products)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Loaded {len(products)} products from {file_path}'
                )
            )

        # Bulk create all products
        try:
            Product.objects.bulk_create(all_products)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully loaded total of {len(all_products)} products'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error bulk creating products: {str(e)}'
                )
            )