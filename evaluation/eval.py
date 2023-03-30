import pandas as pd

import data_proccessing


# from data_proccessing import pre_processing
# # from utils import utils_one
# # from spacy_train_assets.utils import utils


class Eval():
    def __init__(self, model_path) -> None:
        pass

    def eval_model(self):
        """This function will load an existing spacy model and evaluate it on the test and dev set.

        About:
            The evaluation will print out a dataframe with various statistics about the models performance.
        """
