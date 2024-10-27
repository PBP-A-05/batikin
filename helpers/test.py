import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    data = []
    
    # Open the CSV file and read its content
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')  # Assuming tab-separated file
        
        for row in csv_reader:
            # Convert each row to a dictionary
            data.append({
                "Nama Wisata": row["Nama Wisata"],
                "Jam Buka Tutup": row["Jam Buka Tutup"],
                "Nomor Telepon": row["Nomor Telepon"],
                "Link Google Map": row["Link Google Map"],
                "Website": row["Website"],
                "Gambar": row["Gambar"],
                "Deskripsi": row["Deskripsi"]
            })
    
    # Write the list of dictionaries to a JSON file
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# Replace 'input.csv' with your CSV file path and 'output.json' with your desired JSON output path
csv_file_path = 'Dataset Batikin - Wisata Batik.csv'
json_file_path = 'workshop.json'
csv_to_json(csv_file_path, json_file_path)
