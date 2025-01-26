import json

# Read the original dealerships.json
with open('database/data/dealerships.json', 'r') as f:
    data = json.load(f)

# Convert to Django fixture format
fixtures = []
for dealer in data['dealerships']:
    fixtures.append({
        "model": "djangoapp.dealer",
        "pk": dealer['id'],
        "fields": {
            "city": dealer['city'],
            "state": dealer['state'],
            "st": dealer['st'],
            "address": dealer['address'],
            "zip": dealer['zip'],
            "lat": dealer['lat'],
            "long": dealer['long'],
            "short_name": dealer['short_name'],
            "full_name": dealer['full_name']
        }
    })
    
# Write the fixture file
with open('djangoapp/fixtures/initial_data.json', 'w') as f:
    json.dump(fixtures, f, indent=2) 