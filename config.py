import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)