#  On the Off-Target Problem of Zero-Shot Multilingual Neural Machine Translation 🗡

`LAVS.py` first computes the language-specific tokens according to the tokenized corpus and original sharing vocab. The number of language-specific tokens can be controlled by the `shareCommonThres` threshold parameter.

After computing, it generates the LAVS vocab and conducts the LAVS tokenization on the original tokenized corpus. 

With the LAVS vocab and the result of LAVS tokenization, the rest Mutilingual NMT training follows the example from [fairseq](https://github.com/facebookresearch/fairseq/tree/main/examples/multilingual). 

---
Detailed code is coming soon!