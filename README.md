# Welcome to Scaling up Supervised Open Information Extraction

## Introduction

In this repository, you will find the data published in the paper `Scaling Up Supervised Information Extraction`, along with the training procedures necessary to train your open information extractor from these data, and finally, you will find evaluation techniques for evaluating your open information extractor.

## Dataset Creation

In the folder titled `dataset_creation`, you will find code to transform QA-SRL 2.0 data into open information extraction data. In `dataset_creation\dataset_creation\lsoie_data.zip` you will find the full LSOIE dataset, containing the following:

* `lsoie_science_train.conll`
* `lsoie_science_dev.conll`
* `lsoie_science_test.conll`
* `lsoie_wiki_train.conll`
* `lsoie_wiki_dev.conll`
* `lsoie_wiki_test.conll`

## Model Training

This repository contains code to train your open information extractor using the allennlp research framework. You will find the models explored in this work specified in the `large_scale_oie` package. This package is broken into a the following components:

* `dataset_readers` which will read in OIE data into training and inference
* `models` where model specifications are made
* `predictors` where predictions are made
* `evaluation` where evalations is made with trained models

To get started training, first convert your chosen LSOIE data into allennlp connl format with the following command in `./large_scale_oie/dataset_readers`:

```python convert_conll_to_onenotes.py --inp extraction_conlls/train.oie.conll --domain train --out onto_notes_conlls/train.gold_conll```

Now that you have your data ready, specify an experiment json in `./experiments`. There you will see an opportunity to specify your train and validation paths. 

Then, you write a training file like `run_training.sh` which, when run `./run_training.sh` will kick off the allennlp framework. 


