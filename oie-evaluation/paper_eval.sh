#!/bin/bash
rm -rf ./new_eval/
mkdir -p ./new_eval/

#python3 benchmark.py --gold=./oie_corpus/test.oie.orig --out=eval/Rnnoie.dat --tabbed=./systems_output/classic_train_rnnoie.txt

#python3 benchmark.py --gold=./oie_corpus/test.oie.orig --out=eval/old_model.dat --tabbed=./systems_output/ls_long_sort_orig_qdist_old_model.txt
python benchmark.py --gold=./oie_corpus/eval.oie.correct.head --out=new_eval/crf_model_conf.dat --tabbed=./systems_output/crf_model_conf.txt
python benchmark.py --gold=./oie_corpus/eval.oie.correct.head --out=new_eval/srl_bert_oie2016_new_conf.dat --tabbed=./systems_output/srl_bert_oie2015_new_conf.txt
python benchmark.py --gold=./oie_corpus/eval.oie.correct.head --out=new_eval/srl_bert_no_science_new_conf.dat --tabbed=./systems_output/srl_bert_noscience_new_conf.txt
python benchmark.py --gold=./oie_corpus/eval.oie.correct.head --out=new_eval/rnnoie_new_conf.dat --tabbed=./systems_output/rnnoie_new_conf.txt
python benchmark.py --gold=./oie_corpus/eval.oie.correct.head --out=new_eval/qdist_new_conf.dat --tabbed=./systems_output/qdist_new_conf.txt


python pr_plot.py --in=./new_eval --out=./new_eval/eval.png
echo "DONE"
