#!/usr/bin/env python
# coding: utf-8

# In[ ]:


########-------------Title File Processed--------###############

def topic_list(filename):
    title=title_file[filename]
    title=title.lower()
    
    title_spacy=nlp(title)
    mapping={token.text:token.pos_ for token in title_spacy}

    token_title=word_tokenize(title)
    topic_spacy=[]
    
    for chunks in title_spacy.noun_chunks:
        topic_spacy.append(chunks.text)
        
    topics=topic_spacy
    
    POS2Remove=["PROPN", "NOUN"]
    if topics==[]:
        for word in token_title:
            test=nlp(word)
            pos_tag=[(token.pos_) for token in test]
            if pos_tag[0] in POS2Remove:
                topics.append(word)

    ##--- processing of topics
    topic_new=[]
    
    for phrase in topics:

        pre_filtered_chunk=[k for k in phrase.split(" ")]
        new=[]
        for token in pre_filtered_chunk:
            if token in mapping:
                if mapping[token]=='PUNCT' or mapping[token]=='DET' or mapping[token]=='PRON':
                    continue
            new.append(token)
        joint=' '.join(new)
        topic_new.append(joint)
        
    
    topics=topic_new
    
    
    if len(topics)==0 or topics==['']:
        topics=token_title
    
    for s in topics:
        if s in ("_",""," ",'[',']','.'):
            topics.remove(s)
    
    #removing duplictate words
    topics=list(set(topics))
    
    return topics

