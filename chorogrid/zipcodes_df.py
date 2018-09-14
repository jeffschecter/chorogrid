import os

import pandas as pd

# Data files
PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "databases", "zipcodes_to_fips.csv")

zipcodes = pd.read_csv(PATH)
