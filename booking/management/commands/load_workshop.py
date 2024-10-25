from django.core.management.base import BaseCommand
import json
from pathlib import Path
from booking.models import Workshop

class Command(BaseCommand):
    help = 'Load workshop data from JSON file into database'

    def load_json_file(self, file_path):
        """Helper function to load and process workshop JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                workshops_data = json.load(f)

            workshops_to_create = []
            for item in workshops_data:
                try:
                    # Split image URLs if they're in a single string with \n
                    workshop = Workshop(
                        title=item['Nama Wisata'],
                        location=item['Link Google Map'],  # Using Google Maps link as location
                        description=item['Deskripsi'],
                        open_time=item['Jam Buka Tutup'],
                        schedule='',  # No schedule field in JSON
                        image_urls=item['Gambar'],
                        rating=0.0  # Default rating as it's not in the JSON
                    )
                    workshops_to_create.append(workshop)
                except KeyError as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Skipping workshop due to missing field: {e} in {file_path}'
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Error processing workshop in {file_path}: {str(e)}'
                        )
                    )
            
            return workshops_to_create
            
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
        # Clear existing workshops
        self.stdout.write('Deleting existing workshops...')
        Workshop.objects.all().delete()
        
        # Define JSON file path
        file_path = 'static/assets/workshop.json'
        
        # Process the JSON file
        self.stdout.write(f'Loading JSON from {file_path}...')
        workshops = self.load_json_file(Path(file_path))

        # Bulk create all workshops
        try:
            Workshop.objects.bulk_create(workshops)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully loaded {len(workshops)} workshops'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error bulk creating workshops: {str(e)}'
                )
            )