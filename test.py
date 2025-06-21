import pandas as pd
import numpy as np

gen5ou_df = pd.read_csv(r"dataset/showdown/showdown.csv")

print(pd.unique(pd.concat([gen5ou_df[f"Pokemon{i}"] for i in range(1, 7)], axis=0)))