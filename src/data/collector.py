import pandas as pd
import os

print("Calgary Economic Analysis Project")
print("="*40)

# Create data directories
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

print("✓ Project directories created")
print("Ready to collect data!")