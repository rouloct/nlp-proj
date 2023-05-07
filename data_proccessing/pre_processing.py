import spacy
import pandas as pd
from pathlib import Path
import typer
from spacy.tokens import DocBin
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher


ASSETS_DIR = Path(__file__).parent.parent / "assets"
CORPUS_DIR = Path(__file__).parent.parent / "corpus"

# This could be a class, but will probably end up as just usefull functions


def make_binary_classification_doc(row: pd.Series, nlp, categories):
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


def make_multi_classification_doc(row: pd.Series, nlp, categories):
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
    cats = doc.cats

    for category in categories:
        if row[category] == 1:
            doc.cats[category] = 1

    return doc


def generate_binary_corpus(df: pd.DataFrame, nlp, categories):
    """Generate .spacy files for a training pipeline.

    Args:
        df (pd.DataFrame): The pandas dataframe containing the data.
        nlp (_type_): The nlp object helping to create the doc.
        categories (_type_): The possible categories.
    """
    docs = [make_binary_classification_doc(
        row, nlp, categories) for index, row in df.iterrows()]

    out_file = CORPUS_DIR / f"{df.name}.spacy"
    out_data = DocBin(docs=docs).to_bytes()
    with out_file.open("wb") as file_:
        file_.write(out_data)


def generate_multiclass_corpus(df: pd.DataFrame, nlp, categories):
    """Generate .spacy files for a training pipeline.

    Args:
        df (pd.DataFrame): The pandas dataframe containing the data.
        nlp (_type_): The nlp object helping to create the doc.
        categories (_type_): The possible categories.
    """
    docs = [make_multi_classification_doc(
        row, nlp, categories) for index, row in df.iterrows()]

    out_file = CORPUS_DIR / f"{df.name}.spacy"
    out_data = DocBin(docs=docs).to_bytes()
    with out_file.open("wb") as file_:
        file_.write(out_data)


def has_hate_word(text: str, nlp, matcher: Matcher) -> bool:
    """A function which checks if a sentence contains 'hate words'

    Args:
        text (str): The sentence being analyzed
        nlp (_type_): The nlp pipeline that contains the Matcher
        matcher (Matcher): The Matcher which checks each sentence

    Returns:
        bool: Whether or not the phrase had hate words.

    Usage:
        nlp = spacy.load("en_core_web_sm")
        matcher = get_hate_matcher(nlp)
        has_hate_word("Fuck you greedo.", nlp=nlp, matcher=matcher)

    """
    doc = nlp(text)  # Create a doc to analyze
    matches = matcher(doc)
    # print("Matches:", [doc[start:end].text for match_id,
    #       start, end in matches])
    if len(matches) > 0:
        return True

    return False


def remove_passive_comments(dataframe):
    """A toplevel function which facilitates the addition of the new dataframe column "has_hate_words".

    Args:
        dataframe (pd.DataFrame): The dataframe which has a column named "text".

    Returns:
        pd.DataFrame : The dataframe with the added in "has_hate_words" column.
    """

    # Create an nlp object for processing the text
    nlp = spacy.load("en_core_web_sm")

    # The main idea is to build a boolean map for the dataframe
    matcher = get_hate_matcher(nlp)

    dataframe["has_hate_words"] = dataframe.text.apply(
        has_hate_word, nlp=nlp, matcher=matcher)

    return dataframe


# TODO The patterns here are pretty weak. Work adding edge cases like :fuuuuuck
def get_hate_matcher(nlp) -> Matcher:
    """A function for storing the patterns we would like to match.

    Args:
        nlp (_type_): The nlp object which provides the vocab.

    Returns:
        Matcher: A Matcher with all of the new patterns added.
    """

    fuck_pat = [
        {"LOWER": {"IN": ["fuck", "fuk", "fuc", "fuq", "fak", "fucker"]}}]
    fag_pat = [
        {"LOWER": {"IN": ["gay", "fag", "fagy", "fag", "faggot", "fuggot", "faggie"]}}]
    trans_pat = [{"LOWER": {"IN": ["trans", "trannie", 'trani', "trany", ""]}}]
    dick_pat = [{"LOWER": {"IN": ["dick", "dicker"]}}]
    bitch_pat = [{"LOWER": {"IN": ["bitch", "biach", "bish"]}}]
    pussy_pat = [{"LOWER": {"IN": ["pus", "pussy", "possy", "p3ssy"]}}]
    whore_pat = [{"LOWER": {"IN": ["whore", "hoe", "cunt"]}}]
    rape_pat = [{"LOWER": {"IN": ["rape", "ape", "r8pe"]}}]
    nigger_pat = [
        {"LOWER": {"IN": ["nig", "n1g", "nigger", "nigg3r", "n1gger"]}}]
    retard_pat = [{"LOWER": {"IN": ["tard", "retard", "tardo", "r-tard"]}}]
    matcher = Matcher(nlp.vocab)
    matcher.add("pattern1", [fuck_pat, fag_pat, trans_pat, dick_pat, bitch_pat,
                pussy_pat, whore_pat, rape_pat, whore_pat, nigger_pat, retard_pat])

    return matcher


def get_hate_matcher_phrase(nlp) -> PhraseMatcher:
    HATE_WORDS = ['fuck you', 'fuck', 'hitler',
                  'Nigger', 'fag', 'faggot', 'pussy']
    matcher = PhraseMatcher(nlp.vocab)
    patterns = list(nlp.pipe(HATE_WORDS))
    matcher.add("hate_words", patterns)
    return matcher


# def main():
#     # Create an nlp object for processing the text
#     nlp = spacy.load("en_core_web_sm")

#     # The main idea is to build a boolean map for the dataframe
#     matcher = get_hate_matcher(nlp)
#     has_hate_word("fuck you Nigger.", nlp=nlp, matcher=matcher)


# if __name__ == "__main__":
#     main()
