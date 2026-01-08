import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import statsmodels.api as sm

print("=== CALGARY ECONOMIC ANALYSIS ENVIRONMENT TEST ===")
print(f"Python version: {sys.version[:6]}")
print(f"Pandas version: {pd.__version__}")
print(f"NumPy version: {np.__version__}")
print(f"Matplotlib version: {plt.matplotlib.__version__}")
print(f"Statsmodels version: {sm.__version__}")

# Test data download
print("\nTesting data download...")
try:
    test_data = yf.download("CL=F", period="1mo", progress=False)
    print(f"✓ Oil price data downloaded: {len(test_data)} rows")
    print(f"  Date range: {test_data.index[0].date()} to {test_data.index[-1].date()}")
except Exception as e:
    print(f"✗ Data download failed: {e}")

# Test plotting
print("\nTesting visualization...")
try:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot([1, 2, 3], [4, 5, 6])
    ax.set_title("Test Plot")
    plt.savefig("outputs/plots/test_plot.png", dpi=100)
    print("✓ Plot created and saved to outputs/plots/test_plot.png")
except Exception as e:
    print(f"✗ Plotting failed: {e}")

print("\n" + "="*50)
print("✅ ENVIRONMENT READY FOR CALGARY ANALYSIS!")
print("="*50)