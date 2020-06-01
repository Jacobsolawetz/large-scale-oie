#!/bin/bash
rm -rf ./science_new_eval/
mkdir -p ./science_new_eval/

#python3 benchmark.py --gold=./oie_corpus/test.oie.orig --out=eval/Rnnoie.dat --tabbed=./systems_output/classic_train_rnnoie.txt

#python3 benchmark.py --gold=./oie_corpus/test.oie.orig --out=eval/old_model.dat --tabbed=./systems_output/ls_long_sort_orig_qdist_old_model.txt
python benchmark.py --gold=./oie_corpus/science_eval.oie.correct.head --out=science_new_eval/crf_noscience.dat --tabbed=./systems_output/ls_long_sort_orig_qdist_old_model_crf_on_science.txt
python benchmark.py --gold=./oie_corpus/science_eval.oie.correct.head --out=science_new_eval/crf_science.dat --tabbed=./systems_output/ls_long_sort_orig_qdist_old_model_crf_science_on_science.txt
python benchmark.py --gold=./oie_corpus/science_eval.oie.correct.head --out=science_new_eval/qdist_noscience.dat --tabbed=./systems_output/ls_long_sort_orig_qdist_old_model_on_science.txt
python benchmark.py --gold=./oie_corpus/science_eval.oie.correct.head --out=science_new_eval/qdist_science.dat --tabbed=./systems_output/ls_long_sort_orig_qdist_old_model_science_on_science.txt
python benchmark.py --gold=./oie_corpus/science_eval.oie.correct.head --out=science_new_eval/srl_bert_noscience.dat --tabbed=./systems_output/srl_bert_no_science_on_science.txt
python benchmark.py --gold=./oie_corpus/science_eval.oie.correct.head --out=science_new_eval/srl_bert_oie2016.dat --tabbed=./systems_output/srl_bert_oie2016_on_science.txt
python benchmark.py --gold=./oie_corpus/science_eval.oie.correct.head --out=science_new_eval/srl_bert_science.dat --tabbed=./systems_output/srl_bert_science_on_science.txt
python benchmark.py --gold=./oie_corpus/science_eval.oie.correct.head --out=science_new_eval/rnnoie.dat --tabbed=./systems_output/classic_full_run_on_science.txt


python pr_plot.py --in=./science_new_eval/ --out=./science_new_eval/eval.png
echo "DONE"
