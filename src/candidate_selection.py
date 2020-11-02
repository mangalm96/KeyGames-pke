#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# --candidate selection--

def cand_select(self,normalization,model):
        
    cand_duplicate=[]
    #iterate through sentences
    for s_id,k in enumerate(self.sentences):

        shift = sum([s.length for s in self.sentences[0:s_id]])

        # join words and use chunking to get candidates of that sentence
        input_text=" ".join(k.words)
        doc=nlp(input_text)
        
        #-------chunking and splitting and/or phrases------------#
        chunk_list=[]
        ptag=[]
        for chunk in doc.noun_chunks:
            
            # a phrase should not contain more than 5 words
            if len(chunk.text.split(' '))<6:
            
                if ' and ' in chunk.text:
    
                    pp=chunk.text.split(' and ')[0].split(' ')
                    found=0
        
                    # if noun phrase contains 'and', then check that the words inside that np should not be repeated/already considered
                    # as chunks before
                    for w in pp:
                        if w in chunk_list:
                            found=found+1
                    if found>=1:
                        continue
                        
                    chunk_list.append(chunk.text.split(' and ')[0])
                    chunk_list.append(chunk.text.split(' and ')[1])
    
                elif ' or ' in chunk.text:
                    pp=chunk.text.split(' or ')[0].split(' ')
                    found=0
                    for w in pp:
                        if w in chunk_list:
                            found=found+1
                    if found>=1:
                        continue
                    chunk_list.append(chunk.text.split(' or ')[0])
                    chunk_list.append(chunk.text.split(' or ')[1])

                else:
                    chunk_list.append(chunk.text)
 
        #-----------------------------------------------------
        
        temp_offset=-1
        length_prev=0
        for chunks in chunk_list:

            pre_filtered=[k for k in chunks.split(" ")]
            candidate_list=[] 
            candidate_string=''
            for phrase in pre_filtered:
                delete=apply_filters(phrase)
                if phrase=='and' or phrase=='or':
                    delete=1
                if delete==0:
                    candidate_list.append(phrase)
            
            candidate_string=' '.join(candidate_list)

            if normalization:
                stem=[stemmer.stem(k) for k in candidate_string.split(" ")] # for topicrank,mprank
            else:
                stem=[k.lower() for k in candidate_string.split(" ")] # for singlerank,positionrank,embedrank where Normalization=None in load_document
        
            new_words=[]
            for word in k.words:
                if word!=',':
                    new_words.append(word.translate(str.maketrans('', '',',')))
                else:
                    new_words.append(word)
            
            ptag2=[]
            for w in candidate_list:
                for s,po in zip(new_words,k.pos):
                    if s==w:
                        ptag2.append(po)
                        break


####--------------POS TAGS IN SENTENCES---------------#####
            
            
            # filtering for singular tokens
            new_lexical=[]
            if len(stem)==1:
                if stem!=['']:
                    if ptag2==[]:
                        test=nlp(candidate_list[0]) 
                        pos_tag=[(token.pos_) for token in test]
                        ptag2=pos_tag
                        if pos_tag[0]=='PROPN' or pos_tag[0]=='X':
                            new_lexical=stem[0]
                        
                        
                    elif ptag2[0]=='PROPN' or ptag2[0]=='X':
                    
#                         print(stem)
                        new_lexical=stem[0]
                    else:
                        continue
                else:
                    continue
            else:
                new_lexical=" ".join(stem)
            
            
            
            lexical_form=new_lexical
            
            self.candidates[lexical_form].lexical_form=stem # stemmed/lowered candidates
            self.candidates[lexical_form].surface_forms.append(candidate_list) # unstemmed/unlowered candidates

            self.candidates[lexical_form].pos_patterns.append(ptag2) # append pos tags created above
            
            
            # offset calculation based on model
            
            if model=="keygames":
                cand_duplicate.append(new_lexical)
                indices = [i for i, x in enumerate(cand_duplicate) if x == lexical_form]
                
                self.candidates[lexical_form].offsets=indices
                self.candidates[lexical_form].sentence_ids.append(s_id)
                
            else:
                
                if k.length==1:
                    self.candidates[lexical_form].offsets.append(shift)
                    self.candidates[lexical_form].sentence_ids.append(s_id)
                 # for offset
                
                else:
                    
                    for i in range(1,k.length):
                        if candidate_string=='':
                            break;
                        nth_word_offset=nth_item(i,candidate_string.split(" ")[0],new_words)
                        if nth_word_offset>(temp_offset+length_prev-1):
                            temp_offset=nth_word_offset
                            offset=shift+nth_word_offset
                            self.candidates[lexical_form].offsets.append(offset)
                            self.candidates[lexical_form].sentence_ids.append(s_id)
                            break;
                    if candidate_string!='':
                        length_prev=len(candidate_list)
            

    # ---candidate selection done ------
    

