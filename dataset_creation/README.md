This folder contains the tools necessary to convert QA-SRL 2.0 data to open information extraction data.

Data contained in this folder includes 'lsoie_data' with the final release of the LSOIE dataset, unzipped breaks into `lsoie_science` and `lsoie_wiki`. The original QA-SRL 2.0 dataset used in this work is included in `qa_srl_2_orig.zip`


Step 1: Create generalized question distribution using `analzye.py` with the QA-SRL file you wish to convert
Step 2: Convert QA-SRL data to LSOIE data with `read_data.py`
