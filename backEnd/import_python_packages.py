import sys
import subprocess


subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'osmnx'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask'])