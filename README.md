# spacy_training_assets
A repository containing various scripts, configs and guides used for training and evaluating spaCy pipelines.

## Folder Overview

* data_processing
* training
* evaluation
* utils
* datasets

### data_processing

This directory is meant to house modules which aid in the scraping and pre-processing of data. The primary goal is to provide functions which make it easy to go from scraping reddig to exporing training data in the .spacy file format.

### training

The Training folder contains various config files, training commands, and notes on training.

### evaluation

The Evaluation script is for evaluating the model on a test dataset. Performance metrics are stored in a csv/json file format.

### utils

This directory is currently empty, but can be used as a common space where functions that may not have an obvious home should go. 

### dataset

This directory is meant to hold the most up to data training, dev, and test datasets. 