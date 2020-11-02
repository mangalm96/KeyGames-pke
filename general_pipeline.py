#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# general pipleine -- user page to run everything

path=os.getcwd()+"/data/input/semeval_input/" # for semeval
# path=os.getcwd()+"/data/input/inspec_input/" # for inspec
# path=os.getcwd()+"/data/input/duc_input/" # for duc 


pos = {'NOUN', 'PROPN', 'ADJ','VERB'}
ct=0
model="keygames"

for filename in sorted(glob.glob(os.path.join(path, '*.txt')),key=numericalSort):

    # initialize keyphrase extraction model
    extractor = pke.unsupervised.SingleRank()

    # 2. load the content of the document.
    extractor.load_document(input=filename)
    
    #3. candidate selection
    cand_select(extractor,normalization=None,model=model)
    
    #4.candidate wighting/ranking
    new_rank(extractor,ct) 
    
    keyphrases_10=get_n_best(extractor,n=10)
#     keyphrases_15 = get_n_best(extractor,n=15)
#     keyphrases_5 = get_n_best(extractor,n=5)
    
    keylist1=[]
    for k in keyphrases_10:
        keylist1.append(k[0])
    
    path_key1=os.getcwd()+"/data/output/semeval_keys/"
    doc_name=filename.split("semeval_input/")[1][:-4] 
    
    name_of_file='{}.key.txt'.format(doc_name)            
    extracted_keyword_file1 = os.path.join(path_key1, name_of_file)
    with open(extracted_keyword_file1, 'w') as f:
        for p in keylist1:
            f.write("%s\n" % p)
    
    print("{}".format(ct))
    ct=ct+1

