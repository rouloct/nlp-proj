import spacy
import pandas as pd
from pathlib import Path
import typer
from spacy.tokens import DocBin
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher


ASSETS_DIR = Path(__file__).parent.parent / "assets"
CORPUS_DIR = Path(__file__).parent.parent / "evaluation/corpus"

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

    for category in categories:
        if row[category] == True:
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
    
    out_file = CORPUS_DIR / f"{df.Name}.spacy"
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

    out_file = CORPUS_DIR / f"{df.Name}.spacy"
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


def get_hate_matcher(nlp) -> Matcher:
    """A function for storing the patterns we would like to match.

    Args:
        nlp (_type_): The nlp object which provides the vocab.

    Returns:
        Matcher: A Matcher with all of the new patterns added.
    """

    cyber_pat = [{"LOWER": {"IN": ["harass", "troll", "stalk", "stalker", "harassing", "trolling"]}}]
    xeno_pat = [{"LOWER": {"IN": ["not welcome", "back to your country"]}}]
    insult_pat = [{"LOWER": {"IN": [ "idiot", "moron", "dumbass", "loser", "scumbag"]}}]
    jew_pat = [{"LOWER": {"IN": ["jew", "hitler"]}}]
    violence_pat = [{"LOWER": {"IN": ["waste of life", "kill", "hurt", "trash", "suicide", "cut", "hang"]}}]
    pedo_pat = [{"LOWER": {"IN": ["pedo",]}}]
    women_pat = [{"LOWER": {"IN": ["woman", "women", "girls"]}}]
    fat_pat = [{"LOWER": {"IN": ["fat", "whale", "worthless", "pathetic", "ugly", "fatso"]}}]
    fuck_pat = [
        {"LOWER": {"IN": ["fuck", "fuk", "fuc", "fuq", "fak", "fucker"]}}]
    gay_pat = [
        {"LOWER": {"IN": ["gay", "fag", "fagy", "fag", "faggot", "fuggot", "faggie", "lgbt", "lgbtq", "dyke"]}}]
    trans_pat = [{"LOWER": {"IN": ["trans", "trannie", 'trani', "trany", "tranny"]}}]
    dick_pat = [{"LOWER": {"IN": ["dick", "dicker"]}}]
    bitch_pat = [{"LOWER": {"IN": ["bitch", "biach", "bish", "slut", "whore", "kitchen"]}}]
    pussy_pat = [{"LOWER": {"IN": ["pus", "pussy", "possy", "p3ssy"]}}]
    whore_pat = [{"LOWER": {"IN": ["whore", "hoe", "cunt"]}}]
    rape_pat = [{"LOWER": {"IN": ["rape", "ape", "r8pe"]}}]
    other_swears = [{"LOWER": {"IN": ["cunt", "asshole"]}}]
    nigger_pat = [
        {"LOWER": {"IN": ["nig", "n1g", "nigger", "nigg3r", "n1gger", "negro"]}}]
    retard_pat = [{"LOWER": {"IN": ["tard", "retard", "tardo", "r-tard"]}}]
    race_pat = [{"LOWER": {"IN": ["chink", "jew", "cracker", "barbarian", "ching chong", "monkey", "redskin"]}}]
    matcher = Matcher(nlp.vocab)
    matcher.add("pattern1", [fuck_pat, insult_pat, other_swears, gay_pat, trans_pat, dick_pat, bitch_pat, jew_pat,
                pussy_pat, cyber_pat, whore_pat, rape_pat, whore_pat, xeno_pat, nigger_pat, retard_pat, race_pat, fat_pat, women_pat, violence_pat, pedo_pat])

    return matcher


def get_hate_matcher_phrase(nlp) -> PhraseMatcher:
    HATE_WORDS = ['fuck you', 'fuck', 'hitler',
                  'Nigger', 'fag', 'faggot', 'pussy']
    matcher = PhraseMatcher(nlp.vocab)
    patterns = list(nlp.pipe(HATE_WORDS))
    matcher.add("hate_words", patterns)
    return matcher


def filter_long_comments(char_limit: int, df: pd.DataFrame) -> pd.DataFrame:
    """A function for filtering pandas dataframes on the length of the text field

    Args:
        char_limit (int): The max number of characters
        df (pd.DataFrame): The dataframe to filter

    Returns:
        pd.DataFrame: A filtered copy of the previous dataframe
    """
    filtered_df = df[df['text'].str.len().between(0, char_limit)]
    return filtered_df

# TODO Implement this function


def filter_reddit_comments(df: pd.DataFrame) -> pd.DataFrame:
    """This function processes reddit comments for useage in datasets.
        1. Remove emojies
        2. Remove blankspace 
        3. Remove Incoherent text
        3. Remove Excessively long text
    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """


# def main():
#     # Create an nlp object for processing the text
#     nlp = spacy.load("en_core_web_sm")

#     # The main idea is to build a boolean map for the dataframe
#     matcher = get_hate_matcher(nlp)
#     has_hate_word("fuck you Nigger.", nlp=nlp, matcher=matcher)


# if __name__ == "__main__":
#     main()
