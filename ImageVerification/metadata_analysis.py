from PIL import Image, ExifTags

def extract_metadata(image_path):
    image = Image.open(image_path)
    exif_data = {}
    if hasattr(image, '_getexif') and image._getexif() is not None:
        for tag, value in image._getexif().items():
            tag_name = ExifTags.TAGS.get(tag, tag)
            exif_data[tag_name] = value
    return exif_data


image_path = "Sample Images/IMG_2348.HEIC"
metadata = extract_metadata(image_path)

if metadata:
    print("✅ Metadata found:")
    for key, value in metadata.items():
        print(f"{key}: {value}")
else:
    print("⚠️ No EXIF metadata found — possible re-upload or altered image.")
    print("➡️ Switching to visual similarity detection instead.")

def analyze_metadata(metadata):
    issues = []

    required_fields = ['DateTime', 'Make', 'Model']
    for field in required_fields:
        if field not in metadata:
            issues.append(f"Missing metadata field: {field}")

    if 'DateTime' in metadata:
        if "202" not in metadata['DateTime']:  # rough validation
            issues.append(f"Suspicious DateTime: {metadata['DateTime']}")

    if 'GPSInfo' not in metadata:
        issues.append("No GPS metadata present")

    return issues

issues = analyze_metadata(metadata)
print("Metadata Issues:", issues)

def compare_metadata(meta1, meta2):
    similarity = 0
    total_fields = 0

    for key in set(meta1.keys()).intersection(set(meta2.keys())):
        total_fields += 1
        if str(meta1[key]) == str(meta2[key]):
            similarity += 1

    if total_fields == 0:
        return 0.0

    return similarity / total_fields  

score = compare_metadata(metadata, extract_metadata("Sample Images/IMG_2348.HEIC"))
print(f"Metadata consistency score: {score:.2f}")

def get_metadata_consistency(image_path_1, image_path_2=None):
    meta1 = extract_metadata(image_path_1)
    issues = analyze_metadata(meta1)
    score = None

    if image_path_2:
        meta2 = extract_metadata(image_path_2)
        score = compare_metadata(meta1, meta2)

    return {
        "issues": issues,
        "consistency_score": score
    }

result = get_metadata_consistency("Sample Images/IMG_2348.HEIC", "Sample Images/IMG_2349.HEIC")
print(result)