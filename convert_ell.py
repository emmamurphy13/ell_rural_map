import csv, json, sys
from collections import defaultdict

# Load all languages per school from the languages file, ranked by prevalence
languages_by_entity = defaultdict(list)
languages_file = '/Users/emmamurphy/dataProjects/2023-24_ELL_Home_Languages.csv'
try:
    with open(languages_file) as lf:
        for row in csv.DictReader(lf):
            eid = row['ENTITY_CD'].strip()
            rank = int(row['LANGUAGE_RANK'])
            lang = row['HOME_LANGUAGE'].strip()
            languages_by_entity[eid].append((rank, lang))
    for eid in languages_by_entity:
        languages_by_entity[eid].sort()
        languages_by_entity[eid] = [l for _, l in languages_by_entity[eid]]
except FileNotFoundError:
    sys.stderr.write(f"Warning: languages file not found at {languages_file}\n")

# Load K-12 total ELL enrollment by entity
k12_enrollment_by_entity = {}
enrollment_file = '/Users/emmamurphy/dataProjects/migranted/2023-24_ELL_Enrollment.csv'
try:
    with open(enrollment_file) as ef:
        for row in csv.DictReader(ef):
            eid = row['ENTITY_CD'].strip()
            val = row.get('NUM_TOTAL_ELL', '').strip()
            try:
                k12_enrollment_by_entity[eid] = int(float(val)) if val else None
            except ValueError:
                k12_enrollment_by_entity[eid] = None
except FileNotFoundError:
    sys.stderr.write(f"Warning: enrollment file not found at {enrollment_file}\n")

features = []
reader = csv.DictReader(sys.stdin)
for row in reader:
    per_grad = row.get('PER_GRAD', '').strip()
    total_enrolled = row.get('TOTAL_ENROLLED', '').strip()
    num_grad = row.get('NUM_GRAD', '').strip()
    num_dropout = row.get('NUM_DROPOUT', '').strip()
    per_dropout = row.get('PER_DROPOUT', '').strip()
    locale_cat = row.get('LOCALE_CAT', '').strip()

    # Skip rows with no locale (couldn't be matched to NCES data)
    if not locale_cat:
        continue

    try:
        enrolled = int(float(total_enrolled)) if total_enrolled else 0
    except ValueError:
        enrolled = 0

    if enrolled == 0:
        continue

    try:
        grad_rate = float(per_grad) if per_grad and per_grad != '-' else None
    except ValueError:
        grad_rate = None

    try:
        grads = int(float(num_grad)) if num_grad and num_grad != '-' else None
    except ValueError:
        grads = None

    try:
        dropouts = int(float(num_dropout)) if num_dropout and num_dropout != '-' else None
    except ValueError:
        dropouts = None

    try:
        dropout_rate = float(per_dropout) if per_dropout and per_dropout != '-' else None
    except ValueError:
        dropout_rate = None

    # Build geometry — null if no coordinates (school still included for stats)
    lat = row.get('LAT', '').strip()
    lon = row.get('LON', '').strip()
    try:
        geometry = {"type": "Point", "coordinates": [float(lon), float(lat)]} if lat and lon else None
    except ValueError:
        geometry = None

    eid = row.get('ENTITY_CD', '').strip()
    features.append({
        "type": "Feature",
        "geometry": geometry,
        "properties": {
            "name": row.get('ENTITY_NAME', ''),
            "total_enrolled": enrolled,
            "k12_enrolled": k12_enrollment_by_entity.get(eid),
            "per_grad": grad_rate,
            "num_grad": grads,
            "per_dropout": dropout_rate,
            "num_dropout": dropouts,
            "locale": locale_cat,
            "is_rural": row.get('IS_RURAL', '') == 'True',
            "city": row.get('MCITY', ''),
            "state": row.get('MSTATE', ''),
            "home_language": row.get('HOME_LANGUAGE', '').strip() or None,
            "home_languages": languages_by_entity.get(eid) or None,
        }
    })

geojson = {"type": "FeatureCollection", "features": features}
print(json.dumps(geojson))
sys.stderr.write(f"Converted {len(features)} features\n")
