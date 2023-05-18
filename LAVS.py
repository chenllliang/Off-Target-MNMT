from tqdm import tqdm
import os
import numpy as np
import string
import unicodedata

SHAREVOCAB_PATH=""
SHAREVOCAB=[]


with open(SHAREVOCAB_PATH,"r") as f:
    for i in f.readlines():
        tok = i.strip().split()[0]
        SHAREVOCAB.append(tok)

def get_sorted_dict(files,path):
    local_dic={}
    for i in tqdm(files):
        with open(i,"r") as f:
            for i in f.readlines():
                toks = i.strip().split()
                for j in toks:
                    if j in local_dic.keys():
                        local_dic[j] += 1
                    else:
                        local_dic[j] = 1
    
    local_dic = sorted(local_dic.items(), key=lambda item:-item[1])
    with open(path+".dict.txt","w") as f:
        for i,j in local_dic:
            f.write(i+" "+str(j)+"\n")

def get_sorted_dict_temp(files,path,temp=1):
    local_dic={}
    num_sents={}
    ratio={}

    print("computing sents and temperature")

    for i in tqdm(files):
        with open(i,"r") as f:
            sents = len(f.readlines())
            lang = i.split(".")[-1]
            if lang in num_sents.keys():
                num_sents[lang] += sents
            else:
                num_sents[lang] = sents
    
    original_ratio = { i:j/sum(num_sents.values()) for i,j in num_sents.items()}

    t_total = sum( [i**(1/temp) for i in original_ratio.values()])
    scale_after_t = { i: 1/(j**(1/temp)/t_total) for i,j in original_ratio.items()}

    print(scale_after_t)
            
    for i in tqdm(files):
        with open(i,"r") as f:
            lang = i.split(".")[-1]
            for i in f.readlines():
                toks = i.strip().split()
                for j in toks:
                    if j in local_dic.keys():
                        local_dic[j] += int(1*scale_after_t[lang])
                    else:
                        local_dic[j] = int(1*scale_after_t[lang])
    
    local_dic = sorted(local_dic.items(), key=lambda item:-item[1])
    with open(path+".dict.resample1.txt","w") as f:
        for i,j in local_dic:
            f.write(i+" "+str(j)+"\n")

def getVocab(shareVocab,spmFile):
    vocab = {i:0 for i in shareVocab}
    if isinstance(spmFile,list):
        for v_file in spmFile:
            with open(v_file,"r") as f:
                for i in tqdm(f.readlines()):
                    toks = i.strip().split()
                    for j in toks:
                        if j in vocab.keys():
                            vocab[j] += 1
                        else:
                            vocab[j] = 1
    else:
        with open(spmFile,"r") as f:
            for i in tqdm(f.readlines()):
                toks = i.strip().split()
                for j in toks:
                    if j in vocab.keys():
                        vocab[j] += 1
                    else:
                        vocab[j] = 1
    return vocab

def LAVS(shareVocab:list,vocabFromLanguages:dict,shareCommonThres=50):
    # return new vocabs for each language and the compression rate compared to separate vocab in theory
    # The is the implementation of LAVS algorithm, the default frenquency threshold is 50
    # The number of language-specific tokens can be controlled by the shareCommonThres.
    originalSize = len(shareVocab)*len(vocabFromLanguages)
    resultVocab = {i:{} for i in vocabFromLanguages.keys()}
    for token in shareVocab:
        commonNums = 0
        confilictLanguages = []
        for lan, vocabs in vocabFromLanguages.items():
            if vocabs[token] > shareCommonThres:
                commonNums += 1 # if the token appears in more than 1 languages, then it is a shareCommonWord
                confilictLanguages.append(lan)
        if commonNums >= 2 :
            # conflict , need to split vocab
            for i in resultVocab.keys():
                if i not in confilictLanguages:
                    resultVocab[i][token] = True
                else:
                    resultVocab[i][token] = False
        else:
            for i in resultVocab.keys():
                resultVocab[i][token] = True
    
    # compute theory compressing rate compared to seperated vocab
    numSplitToken=0
    for lan,j in resultVocab.items():
        for flag in j.values():
            if not flag:
                numSplitToken += 1
    
    print("sc thres:",shareCommonThres,"compressing rate in theory: ",str((numSplitToken+len(shareVocab))/originalSize))
    print(numSplitToken+len(shareVocab))

    return resultVocab

def getVocabs(langs):
    result={}
    for i in langs:
        print("computing vocab for",i)
        if i!="en_XX":
            vocab = getVocab(SHAREVOCAB,"example_corpus/train.spm.%s-en_XX.%s"%(i,i))
            result[i] = vocab
        else:
            vocab = getVocab(SHAREVOCAB,"example_corpus/train.all.en_XX")
            result[i] = vocab
    return result

def generate_corpus_with_LAVS_vocab(file,out_dir,lang_id,vocab):
    out = open(out_dir,"w")
    srcs = open(file,"r").readlines()
    lang_id = lang_id.split("_")[0]
    for i in srcs:
        toks = i.strip().split(" ")
        new_toks = [j+"_"+lang_id if vocab.get(j,True)==False and len(j)>1 and not unicodedata.category(j[1]).startswith("P") and not j[1].isdigit() else j for j in toks]
        out.write(" ".join(new_toks)+"\n")
    out.close()

if __name__=="__main__":
    import os
    langs=("en_XX","cs_CZ","de_DE","et_EE","fi_FI","fr_XX","gu_IN","hi_IN","lv_LV","ro_RO","tr_TR")
    root_dir="training_corpus"
    tgt_dir="LAVS_Corpus"

    corpus_vocabs = getVocabs(langs)
    thres5_LAVS_VOCAB = LAVS(SHAREVOCAB,corpus_vocabs,5)

    print("Begin LAVS Tokenization with threshold 5, src_dir:%s, tgt_dir:%s, vocab_info:%s"%(root_dir,tgt_dir,"example_vocabs/multilingual_vocab_info_54k.info"))
    for i in tqdm(os.listdir(root_dir)):
        generate_corpus_with_LAVS_vocab(os.path.join(root_dir,i),os.path.join(tgt_dir,i),i[-5:],thres5_LAVS_VOCAB[i[-5:]])

    print("compute lavs vocab using the result after lavs tokenization")
    get_sorted_dict(["LAVS_Corpus/test.spm.%s-en_XX.%s"%(i,i) for i in langs]+["LAVS_Corpus/test.spm.%s-en_XX.en_XX"%(i) for i in langs],"example_vocabs/lavs_vocab")

