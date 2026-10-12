from pathlib import Path
import subprocess, sys
root=Path(__file__).resolve().parent
for script in ['fundamentals.py','analysis.py']:
    subprocess.run([sys.executable,str(root/'src'/script)],check=True)
print('Completed. See outputs/ and data/.')
