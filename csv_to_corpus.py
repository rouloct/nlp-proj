import spacy
import pandas as pd
from pathlib import Path
import typer
from spacy.tokens import DocBin

ASSETS_DIR = Path(__file__).parent.parent / "assets"
CORPUS_DIR = Path(__file__).parent.parent / "corpus"


def make_doc(row: pd.Series, nlp, categories):
    """A function which converts a pandas series to a doc useable in spaCy training.

    Args:
        row (pd.Series): The row to be converted.
        nlp (spacy.Nlp): The nlp object used to make the spaCy.Doc object
        categories (list): The list of potential categories for a text entry. 

    Returns:
        spacy.Doc : The labeled doc
    """
    doc = nlp(row["text"])

    # All categories other than the true ones get value 0
    doc.cats = {category: 0 for category in categories}

    doc.cats[row["label"]] = 1
    return doc


def generate_corpus(df: pd.DataFrame, nlp, categories):
    """Generate .spacy files for a training pipeline.

    Args:
        df (pd.DataFrame): The pandas dataframe containing the data.
        nlp (_type_): The nlp object helping to create the doc.
        categories (_type_): The possible categories.
    """
    docs = [make_doc(row, nlp, categories) for index, row in df.iterrows()]

    out_file = CORPUS_DIR / f"{df.name}.spacy"
    out_data = DocBin(docs=docs).to_bytes()
    with out_file.open("wb") as file_:
        file_.write(out_data)
