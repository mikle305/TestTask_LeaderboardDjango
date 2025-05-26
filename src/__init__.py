import sys
import os


src_path = os.path.abspath("src")
if src_path not in sys.path:
    sys.path.append(src_path)
