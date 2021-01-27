# Welcome to Scaling up Supervised Open Information Extraction

## Introduction

In this repository, you will find the data published in the paper `LSOIE: A Large-Scale Dataset for Supervised Open Information Extraction`, along with the training procedures necessary to train your open information extractor from these data, and finally, you will find evaluation techniques for evaluating your open information extractor.

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

In the models folder there are a few options available to use:

* the vanilla `rnnoie` model
* the `rnnoie` model with a crf output layer
* the `srl_bert` model adapted for OIE

### Prepare Data for Training
To get started training, first convert your chosen LSOIE data into allennlp connl format with the following command in `./large_scale_oie/dataset_readers`:

```python convert_conll_to_onenotes.py --inp extraction_conlls/train.oie.conll --domain train --out onto_notes_conlls/train.gold_conll```

### Specify and Run Experiment

Now that you have your data ready, specify an experiment json in `./experiments`. There you will see an opportunity to specify your train and validation paths. 

Then, you write a training file like `run_training.sh` which, when run `./run_training.sh` will kick off the allennlp framework. Model weights and tensorboard logs are saved in `./results'.

## Making Predictions

Once you have trained your open information extractor, you can use it to make some predictions!

The predictor is built into the `large_scale_oie/evaluation` folder and it is pre configured with the lsoie test set, but you can change that the a txt file of any sentences you would like. To predict run:

``` python large_scale_oie/evaluation/predict_conll.py --in results/srl_bert_no_science/ --out large_scale_oie/evaluation/srl_bert_noscience.conll```

where results are the checkpoints of your trained model. It will by default take `best.th`. 

## Performing Evaluation

The evaluation script here corrects the original `Supervised Open Information Extraction` in that it does not invert confidence estimates and looks for the syntactic head match from the gold extraction argument, rather than lexical overlap, which has many downfalls. 

To use the evaluation script after prediction, you must first convert to tabbed extractions using the following command:

```python large_scale_oie/evaluation/trained_oie_extractor.py --in large_scale_oie/evaluation/ls_long_sort_orig_qdist_old_model_crf_on_science.conll --out large_scale_oie/evaluation/ls_long_sort_orig_qdist_old_model_crf_on_science.txt```

This will take the predictions made by the extractor and transform them into confidences that can be thresholded during eval. 

Now you move to the folder, `oie-evaluation` and you have a couple of options for a test set:

* `eval.oie` new test set for LSOIE
* `test.oie.orig` old test set for rnnoie
* `eval.oie.correct.head` new test set with correct syntactic head match
* `test.oie.orig.correct.head` old test set with correct styntatctic head match

Running the evaluation command

```python3 benchmark.py --gold=./oie_corpus/eval.oie --out=eval/srl_bert_oie2016.dat --tabbed=./systems_output/ls_long_sort_orig_qdist_old_model_new_eval.txt```

And example evaluation series to create eval plots is in the file

```oie_eval/paper_eval.sh```

## Please Stay in Touch

If you have encountered this work and you are interested in building upon it, please reach out! Many pieces shifted during the research process and I can certainly be a resource for you as you discover the contents herein. 


