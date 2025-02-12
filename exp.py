import os
import django
import sys

# Add project directory to sys.path
sys.path.append("/home/jimmy/Desktop/POS/pos")

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pos_system.settings")  # Replace with your actual project name
django.setup()

# Now import Django models
import json
from django.core.serializers import deserialize
from django.apps import apps
from django.db import transaction

# Load JSON data
with open("backup_data.json", "r") as f:
    data = json.load(f)

# Step 1: Import ContentType first
from django.contrib.contenttypes.models import ContentType
if "contenttypes.ContentType" in data:
    print("Importing ContentTypes...")
    for obj in deserialize("json", json.dumps(data["contenttypes.ContentType"])):
        obj.save()
    print("ContentTypes imported successfully!")

# Step 2: Import all other models
with transaction.atomic():
    for model_name, objects in data.items():
        if model_name == "contenttypes.ContentType":  # Skip ContentType (already imported)
            continue

        model = apps.get_model(model_name)
        print(f"Importing {model_name}...")

        for obj in deserialize("json", json.dumps(objects)):
            obj.save()

print("All data imported successfully into PostgreSQL!")
