import json
from django.core.serializers import serialize
from django.apps import apps

# Get all installed models
models = apps.get_models()

data = {}

# Extract data from each model
for model in models:
    model_name = model._meta.label
    data[model_name] = json.loads(serialize("json", model.objects.all()))

# Save to JSON file
with open("backup_data.json", "w") as f:
    json.dump(data, f, indent=4)

print("All data exported successfully!")
