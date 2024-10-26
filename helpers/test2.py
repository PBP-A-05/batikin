import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    data = []
    
    # Open the CSV file and read its content
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')  # Assuming tab-separated file
        
        for row in csv_reader:
            # Split image URLs by comma and strip whitespace
            image_urls = [url.strip() for url in row["Foto (dalam bentuk link) bisa lebih 1 link"].split(',')]
            
            # Convert each row to the specified JSON structure
            data.append({
                "Store URL": row["Link Toko"],
                "Store Address": row["Alamat Fisik"],
                "Product Name": row["Nama Produk"],
                "Price": row["Harga"],
                "Image URLs": image_urls,
                "Additional Info": row["Deksripsi"],
                "Product Link": row["Link Toko"]
            })
    
    # Write the list of dictionaries to a JSON file
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# Replace 'input.csv' with your CSV file path and 'output.json' with your desired JSON output path
csv_file_path = 'Dataset Batikin - Sesuatu yang jogja.csv'
json_file_path = 'sesuatu_jogja.json'
csv_to_json(csv_file_path, json_file_path)
