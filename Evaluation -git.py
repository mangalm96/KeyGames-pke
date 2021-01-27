
# coding: utf-8

# In[20]:


"""
The "evaluate()" function assumes that 
    1. There are two different folders containing assigned & extracted keyphrases for all the documents in a dataset. 
    2. Each keyphrase is seperated by a "/n"
    3. The assigned & extracted keyphrases have been processed in sync (i.e, if assigned keyphrase is stemmed so are extracted keyphrases (SemEval))

The "keyphrase extraction() function" already creates, processes & saves extracted files in sync with assigned keyphrases for the 3 datasets (Inspec, SemEval, DUC-2001). 
Further, we are providing a processed version of assigned keyfiles for these 3 datasets so that they can be simply plugged into the evaluate() function.

In case a new dataset is tested - it will require pre-processing of extracted & assigned keyphrases before evaluating keyphrase extraction algorithms

"""


import glob
import os
import re


def evaluate (path_assigned, path_extracted):
    """
    Arguments: Path to directories where assigned & extracted keyphrases are stored
    Output: Precision, Recall and F-score across the dataset

    """
    extracted_keyfiles=[]
    assigned_keyfiles=[]

    for filename in glob.glob(os.path.join(path_extracted, '*.txt')):
        extracted_keyfiles.append((open(filename).read().split('\n'))[:-1]) # output as list of list. Each list contains words of one doc

    for filename in glob.glob(os.path.join(path_assigned, '*.txt')):
        assigned_keyfiles.append((open(filename).read().split('\n'))[:-1]) # output as list of list. Each list contains words of one doc

    matched=[]

    for key1,key2 in zip(extracted_keyfiles,assigned_keyfiles):
        try:
            matched.append(list(set(key1)&set(key2))) # intersection for matchedkey words
        except:
            matched.append(list(set(key1)))


    tp=[]
    precision=[]
    recall=[]

    matched_combined_d=[]
    for i,match in enumerate(matched):

        matched_combined_d.append(len(match))
        tp.append(len(match)) # no. of true positives or matched keywords

        try:
            precision.append(len(match)/len(extracted_keyfiles[i]))
        except:
            precision.append(0)

        try:
            recall.append(len(match)/len(assigned_keyfiles[i]))
        except:
            recall.append(1) #why?


    f_score=[]
    for p,r in zip(precision,recall):
        if p==0 and r==0:
            f_score.append(0)
        else:
            f_score.append(2*p*r/(p+r))



    #micro-averaged
    length_assigned=[]
    for num,i in enumerate(assigned_keyfiles):
        try:
            length_assigned.append(len(i))
        except:
            length_assigned.append(0)

    length_extracted_keyfiles=[]
    for i in extracted_keyfiles:
        length_extracted_keyfiles.append(len(i))    

    micro_avg_precision= sum(tp)/ sum(length_extracted_keyfiles)
    micro_avg_recall= sum(tp)/ sum(length_assigned)
    micro_avg_fscore= 2*micro_avg_precision*micro_avg_recall/(micro_avg_recall+micro_avg_precision)

        
    return micro_avg_precision, micro_avg_recall, micro_avg_fscore



#Path to assigned keyphrase files
path_assigned= '/Users/arnavsaxena/Desktop/KG_diff/test/assigned/'
#Path to extracted keyphrase files
path_extracted= '/Users/arnavsaxena/Desktop/KG_diff/test/extracted/'

scores=evaluate(path_assigned, path_extracted)


print("\n----SCORES:--------\n")    
print("Micro avg precision: {}".format(scores[0]))
print("Micro avg recall: {}".format(scores[1]))
print("Micro avg fscore: {}".format(scores[2]))


