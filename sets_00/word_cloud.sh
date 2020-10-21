#!/bin/bash
python3 word_cloud.py \
		--pairings_file ../texts/derived/pairs.npy \
		--dictionary_pt ../texts/derived/dictionary.txt
