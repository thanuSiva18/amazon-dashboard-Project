try:
    import pandas
    import matplotlib
    import seaborn
    import openpyxl
    import jupyter
    import numpy
    print("✅ All packages are installed.")
except ImportError as e:
    print("❌ Missing:", e.name)
