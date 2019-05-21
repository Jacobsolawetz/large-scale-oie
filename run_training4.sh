allennlp train experiments/ls_long_sort_orig_qdist_science_old_model.json -s ~/large-scale-oie/results/ls_long_sort_orig_qdist_science_old_model --include-package large_scale_oie
python large_scale_oie/evaluation/predict_conll.py --in results/ls_long_sort_orig_qdist_science_old_model/ --out large_scale_oie/evaluation/ls_long_sort_orig_qdist_science_old_model.conll

