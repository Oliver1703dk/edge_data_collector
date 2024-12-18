# Required imports
from datetime import datetime  # For generating ISO 8601 timestamps


class MetadataHandler:
    @staticmethod
    def add_metadata(data, camera_id):
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "location": "50.8503,4.3517",  # Example GPS coordinates
            "camera_id": camera_id
        }
        return {**data, **metadata}



