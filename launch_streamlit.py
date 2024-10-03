import subprocess
import os

filename = "main.py"  # Ensure this matches your actual Streamlit file name
subprocess.Popen(f"streamlit run {filename} > NUL", shell=True)
