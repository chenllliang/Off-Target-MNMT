from tqdm import tqdm
import os
import numpy as np
import string
import unicodedata
import os





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
    with open(path,"w") as f:
        for i,j in local_dic:
            f.write(i+" "+str(j)+"\n")

    return local_dic

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

def getVocabs(langs,corpus_dir):
    result={}
    for i in langs:
        print("computing vocab for",i)
        if i!="en":
            vocab = getVocab(SHAREVOCAB,corpus_dir+"/opus.en-%s-dev.%s"%(i,i))
            result[i] = vocab
        else:
            vocab = getVocab(SHAREVOCAB,corpus_dir+"/opus_dev.all.en") # concat all english corpus into one file
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

    langs=('be', 'oc', 'he', 'sq', 'fy', 'da', 'mg', 'hi', 'bs', 'li', 'ca', 'zh', 'ml', 'si', 'am', 'mk', 'ur', 'hu', 'tr', 'sr', 'gl', 'nl', 'nn', 'sk', 'my', 'pl', 'ug', 'xh', 'eo', 'vi', 'sv', 'tt', 'tk', 'pt', 'or', 'ig', 'as', 'af', 'gu', 'th', 'ne', 'rw', 'ja', 'bg', 'ga', 'uz', 'cs', 'nb', 'bn', 'sh', 'az', 'fr', 'et', 'tg', 'lt', 'hr', 'en', 'se', 'kk', 'ms', 'yi', 'ku', 'fi', 'ps', 'km', 'no', 'ro', 'ta', 'ka', 'el', 'eu', 'gd', 'uk', 'br', 'te', 'ky', 'fa', 'ha', 'is', 'es', 'ru', 'zu', 'it', 'sl', 'mt', 'de', 'wa', 'lv', 'cy', 'kn', 'pa', 'mr', 'ko', 'ar', 'id')
    # 95 example languages, use the dev split to compute the LAVS vocab for convenience. In real application, the training set should be used.
 
    root_dir="./example_corpus/opus_dev_tokenized"
    tgt_dir="./lavs_tokenized_corpus"

    SHAREVOCAB_PATH="./example_corpus/shared_vocab.txt"
    SHAREVOCAB=[]
    LAVS_THRES=20

    with open(SHAREVOCAB_PATH,"r") as f:
        for i in f.readlines():
            tok = i.strip().split()[0]
            SHAREVOCAB.append(tok)

    corpus_vocabs = getVocabs(langs,root_dir)
    thres5_LAVS_VOCAB = LAVS(SHAREVOCAB,corpus_vocabs,LAVS_THRES)

    print("Begin LAVS Tokenization with threshold %s, src_dir:%s, tgt_dir:%s, original vocab:%s"%(LAVS_THRES,root_dir,tgt_dir,SHAREVOCAB_PATH))
    for i in tqdm(os.listdir(root_dir)):
        generate_corpus_with_LAVS_vocab(os.path.join(root_dir,i),os.path.join(tgt_dir,i),i[-2:],thres5_LAVS_VOCAB[i[-2:]])

    print("compute lavs vocab using the result after lavs tokenization")
    lavs_dict = get_sorted_dict(["%s/opus.en-%s-dev.%s"%(tgt_dir,i,i) for i in langs if i!="en"]+["%s/opus.en-%s-dev.en"%(tgt_dir,i) for i in langs if i!="en"],"./lavs_vocab.txt")

    print("there are %s tokens in original vocab, %s tokens in LAVS vocab, you can adjust the size of LAVS vocab by changing the LAVS_THRES parameter"%(len(SHAREVOCAB),len(lavs_dict)))
    print("the new vocab is saved in ./lavs_vocab.txt, you can use it to train your model")
