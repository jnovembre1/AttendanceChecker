from datasets import load_dataset
from deepface import DeepFace
import psycopg2
from PIL import Image
import io
import requests

# PostgreSQL database connection details
DB_NAME = "mydb"
DB_USER = "myuser"
DB_PASSWORD = "mypassword"
DB_HOST = "localhost"
DB_PORT = "5432"

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)
cur = conn.cursor()

# Load LAION-Face dataset from Hugging Face
print("Loading LAION-Face dataset...")
dataset = load_dataset("FacePerceiver/laion-face", split="train", streaming=True)

# Process each sample in the dataset
print("Processing dataset...")
for i, sample in enumerate(dataset):
    if i >= 1000:  # Limit to 1000 samples for testing (adjust as needed)
        break

    try:
        # Download image from URL
        response = requests.get(sample["image_url"])
        img = Image.open(io.BytesIO(response.content))

        # Generate embedding using DeepFace
        embedding = DeepFace.represent(img, model_name="VGG-Face")[0]["embedding"]

        # Insert student into database (using image URL as name for demonstration)
        cur.execute(
            """
            INSERT INTO students (name, rocket_number)
            VALUES (%s, %s)
            ON CONFLICT (rocket_number) DO NOTHING RETURNING id;
            """,
            (sample["image_url"][:100], f"RN{hash(sample['image_url']) % 100000}"),
        )
        result = cur.fetchone()
        if result:
            student_id = result[0]
        else:
            cur.execute(
                "SELECT id FROM students WHERE rocket_number = %s",
                (f"RN{hash(sample['image_url']) % 100000}",),
            )
            student_id = cur.fetchone()[0]

        # Insert embedding into face_embeddings table
        cur.execute(
            """
            INSERT INTO face_embeddings (student_id, embedding)
            VALUES (%s, %s);
            """,
            (student_id, memoryview(bytearray(embedding))),
        )
        conn.commit()

        print(f"Processed sample {i+1}: {sample['image_url']}")

    except Exception as e:
        print(f"Error processing sample {i+1}: {e}")

# Close database connection
cur.close()
conn.close()
print("Dataset processing complete.")
