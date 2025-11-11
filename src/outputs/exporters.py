thonimport json
import os

class Exporter:
    def export_to_json(self, data, file_path):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data exported to {file_path}")