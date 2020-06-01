# Welcome to Scaling up Supervised Open Information Extraction

## Introduction

In this repository, you will find the data published in the paper "Scaling Up Supervised Information Extraction", along with the training procedures necessary to train your open information extractor from these data, and finally, you will find evaluation techniques for evaluating your open information extractor.

## Dataset Creation

In the folder titled `dataset_creation`, you will find code to transform QA-SRL 2.0 data into open information extraction data. In `dataset_creation\dataset_creation\lsoie_data.zip` you will find the full LSOIE dataset, containing the following:

*`lsoie_science_train.conll`
*`lsoie_science_dev.conll`
*`lsoie_science_test.conll`
*`lsoie_wiki_train.conll`
*`lsoie_wiki_dev.conll`
*`lsoie_wiki_test.conll`

## Model Training

This repository contains code to train your open information extractor using the allennlp research framework. 
