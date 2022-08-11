# Makes relative imports working properly for the environment package
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
