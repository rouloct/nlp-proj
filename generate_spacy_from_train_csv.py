import pandas as pd
from data_processing import pre_processing as pp
import spacy

nlp = spacy.blank("en")

# The amount of data that should be dev data.
DEV_SIZE = 0.15

# Make the dataframe from the file.
df = pd.read_csv("/Users/rory/hate_speech_detector/datasets/hate_detector/train.csv")

# Drop unnamed columns and columns with no text.
df.drop(df.columns[df.columns.str.contains('unnamed',case = False)], axis=1, inplace=True)
df.dropna(inplace=True)

# Rename 'post' to 'text'.
df.rename(columns={"post":"text"}, inplace=True)

# Get the number of rows.
total_rows = df.shape[0]
dev_rows = int(total_rows * DEV_SIZE)

# Randomly reorder the dataframe.
df = df.sample(frac=1)

# Split into dev and train dataframes.
dev_df = df.iloc[:dev_rows]
dev_df.Name = "dev"
train_df = df.iloc[dev_rows:]
train_df.Name = "train"

print(f"Training data length: {len(train_df)}")
print(f"Dev data length: {len(dev_df)}")
print(f"Total data length: {len(dev_df) + len(train_df)}")

# Declare categories.
categories = ['directed_hostility','disrespectful','innapropriate']

# Generate .spacy files
pp.generate_multiclass_corpus(dev_df, nlp, categories)
pp.generate_multiclass_corpus(train_df, nlp, categories)

print(".spacy files generated successfully.")