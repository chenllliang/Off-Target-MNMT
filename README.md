# On the Off-Target Problem of Zero-Shot Multilingual Neural Machine Translation 🎯

This repository provides a fast implementation of the LAVS algorithm described in the paper.

---

LAVS offers an improved vocabulary building method for MNMT (Multilingual Neural Machine Translation).

## Language-Aware Vocabulary Sharing

To use the `LAVS.py` script, follow these steps:

1. Prepare the original shared vocabulary file (same format as `example_corpus/shared_vocab.txt`).
2. Prepare the tokenized **training** corpus for MNMT (same format as `example_corpus/opus_dev_tokenized`). In this example, dev data is used for storage convenience.
3. Run `python ./LAVS/LAVS.py` and adjust the `LAVS_THRES` parameter in the script to control the number of language-specific tokens. A larger `LAVS_THRES` value means fewer language-specific tokens.
4. The new vocabulary will be saved at `./lavs_vocab.txt`, and the LAVS-tokenized training corpus will be saved at `./lavs_tokenized_corpus`.

Please note that if the naming conventions of your data are different, you may need to modify the `LAVS.py` file accordingly.

After LAVS tokenization, some language-specific tokens will be added. For example, "to" could be transformed into "to_en" for English, "to_de" for German. You can use the new vocabulary and LAVS-tokenized files to train the multilingual model.


## Training and Evaluation

To train the multilingual NMT model using the LAVS vocabulary and the LAVS tokenization results, simply follow the example provided in [fairseq](https://github.com/facebookresearch/fairseq/tree/main/examples/multilingual) and train the transformer from scratch.

The only difference in evaluation is that you need to remove the language tag from each decoded token before running detokenization. You can achieve this by running the following command:

```bash
sed 's/_..//g' <lavs_tokenized_file> > <normal_tokenized_file>
```

Training and evaluation scripts will be uploaded soon after cleaning.

## Citation

If you find the paper helpful, please kindly cite it:

```bib
@article{Chen2023OnTO,
  title={On the Off-Target Problem of Zero-Shot Multilingual Neural Machine Translation},
  author={Liang Chen and Shuming Ma and Dongdong Zhang and Furu Wei and Baobao Chang},
  journal={ArXiv},
  year={2023}
}
```
