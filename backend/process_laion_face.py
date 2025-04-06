from datasets import load_dataset
from deepface import DeepFace
import psycopg2
from PIL import Image
import io
import requests
import numpy as np
import albumentations as A
import cv2
# Create an augmentation pipeline for face images
# Use safe transformations that won't distort facial features too much
transform = A.Compose([
    A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.7),
    A.Rotate(limit=10, p=0.5),  # Slight rotation (max 10 degrees)
    A.ImageCompression(quality_lower=80, quality_upper=100, p=0.5),  # JPEG compression simulation
    A.GaussNoise(var_limit=(10.0, 50.0), p=0.5),  # Add gaussian noise
    A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15, p=0.5),
    A.OneOf([
        A.MotionBlur(blur_limit=3, p=0.5),
        A.MedianBlur(blur_limit=3, p=0.5),
        A.GaussianBlur(blur_limit=3, p=0.5),
    ], p=0.3),
])

# Load LAION-Face dataset from Hugging Face
print("Loading LAION-Face dataset...")
dataset = load_dataset("FacePerceiver/laion-face", split="train", streaming=True)

processed_count = 0
max_samples = 1000  # Limit the number of samples to process

try:
    for sample in dataset:
        if processed_count >= max_samples:
            break
            
        try:
            response = requests.get(sample["image_url"], timeout=10)
            response.raise_for_status()
            img = Image.open(io.BytesIO(response.content))
            
            # Apply augmentations
            # First, convert PIL Image to numpy array for Albumentations
            img_np = np.array(img)
            
            # Check if the image is grayscale and convert to RGB if needed
            if len(img_np.shape) == 2:
                img_np = cv2.cvtColor(img_np, cv2.COLOR_GRAY2RGB)
            elif img_np.shape[2] == 1:
                img_np = cv2.cvtColor(img_np, cv2.COLOR_GRAY2RGB)
            elif img_np.shape[2] == 4:  # Handle RGBA images
                img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)
                
            # Apply the augmentation transform
            augmented = transform(image=img_np)
            img_augmented_np = augmented['image']
            
            # Convert back to PIL Image for DeepFace
            img_augmented = Image.fromarray(img_augmented_np)
            
            # Generate embedding using DeepFace
            embedding = DeepFace.represent(img_augmented, model_name="VGG-Face")[0]["embedding"]
            
            # TODO: Store the embedding in your database here
            
            processed_count += 1
            if processed_count % 10 == 0:
                print(f"Processed {processed_count} images")
                
        except requests.RequestException as e:
            print(f"Failed to download image: {e}")
            continue
        except Exception as e:
            print(f"Error processing image: {e}")
            continue

except KeyboardInterrupt:
    print("\nProcessing interrupted by user")
finally:
    print(f"\nFinished processing {processed_count} images")
