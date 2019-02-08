import sys
import os
sys.path.append(os.getcwd())
#learn more about python imports and relative paths
from allennlp.common.testing import AllenNlpTestCase
from allennlp.models.archival import load_archive
from allennlp.predictors import Predictor
from allennlp.data.tokenizers import WordTokenizer
from allennlp.data.tokenizers.word_splitter import SpacyWordSplitter
import json
from large_scale_oie.predictors.oie_predictor import OpenIePredictor
from large_scale_oie.models.oie_model import OieLabeler
import os

if __name__ == "__main__":

    labels = []
    model_path = 'results/classic_fullrun/'
    with open(model_path + 'vocabulary/labels.txt', "r") as vocab:
        for label in vocab:
            labels.append(label.rstrip())
    print(labels)

    archive = load_archive('results/classic_fullrun/model.tar.gz')

    predictor = Predictor.from_archive(archive, 'oie')
    #iterate through sentences
    sentences = 'tests/fixtures/oie_test.jsonl'
    with open(sentences, "r") as sents:
        for sent in sents:
             inp = json.loads(sent)
             result = predictor.predict_json(inp)
             probs = result['class_probabilities']
             

