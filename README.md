#  On the Off-Target Problem of Zero-Shot Multilingual Neural Machine Translation  🎯

This is a fast implementation for LAVS algorithm in the paper.

---

LAVS provides a better vocabulary building method for MNMT.

`LAVS.py` first computes the language-specific tokens according to the tokenized corpus and original sharing vocab. The number of language-specific tokens can be controlled by the `LAVS_THRES` threshold parameter.

After computing, it generates the LAVS vocab and conducts the LAVS tokenization on the original tokenized corpus. 

## Language-Aware Vocabulary Sharing

1. prepare the original shared vocabulary (same format as `example_corpus/shared_vocab.txt`)
2. prepare the tokenized **training** corpus of MNMT (same format as `example_corpus/opus_dev_tokenized`, we use dev data here for storage convinence)
3. `python ./LAVS/LAVS.py` , change the LAVS_THRES parameter in the script to control the number of langauge-specific token. Larger LAVS_THRES means less langauge-specific token.
4. The new vocab is saved at `./lavs_vocab.txt` and the lavs-tokenzied training corpus is saved at `lavs_tokenized_corpus`

You may need to slightly modify the `LAVS.py` file if the naming of your data is different.

After LAVS tokenization, some language-specific tokens would be added. For example "to" -> "to_en". You can use the new vocab and lavs-tokenized files to train the multilingual model.


## Training and Evaluation

With the LAVS vocab and the result of LAVS tokenization, the rest Mutilingual NMT training follows the example from [fairseq](https://github.com/facebookresearch/fairseq/tree/main/examples/multilingual). 

The only different in evaluation is that you need to remove the langauge tag in each decoded token before running detokenization. You can simply do it by running :

`sed 's/_..//g' <lavs_tokenized_file> > <normal_tokenized_file>`


Training and Evaluation scripts will be uploaded soon after cleaning.  


## Citation

If you find the paper helpful, please kindly cite our paper.

```bib
@article{Chen2023OnTO,
  title={On the Off-Target Problem of Zero-Shot Multilingual Neural Machine Translation },
  author={Liang Chen and Shuming Ma and Dongdong Zhang and Furu Wei and Baobao Chang},
  journal={ArXiv},
  year={2023}
}
```


