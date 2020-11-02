#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def new_rank(self,filenum):
    
    word_list=[]
    tuples=list(self.candidates.items())
    for t in tuples:
        word_list.append(t[0])
    
    # title processed and returned
    topic=topic_list(filenum)
    w_t=list()
    w = [0] * len(word_list)
    for t in topic:
        w_t=[]
        for word in word_list:
            w_t.append (similarity(word,t))
        for i in range(len(word_list)) :
            w[i]=w[i] + w_t[i]
    w_new=list(map(lambda x: x/max(w),w))
    
    position_freq_scores=[]
    for candidate in list(self.candidates):
        v = self.candidates[candidate]
        p_f_score=0
        for index in v.offsets:
            p_f_score+=1/(index+1)
        position_freq_scores.append(p_f_score) 
        
    
    p_new=list(map(lambda x: x/max(position_freq_scores),position_freq_scores))
    
    
    con=[sum(x) for x in zip(w_new, p_new)]

    w_sim = [[0.0 for x in range(len(word_list))] for y in range(len(word_list))]
    #creating similarity matrix between candidate words
    for i,word1 in enumerate(word_list):
        for j,word2 in enumerate(word_list):
            simij=similarity(word1,word2)
            w_sim[i][j] = simij

    fuz = [[0.0 for x in range(len(word_list))] for y in range(len(word_list))]
    for i,word1 in enumerate(word_list):
        for j,word2 in enumerate(word_list):
            fuz[i][j] = fuzz.token_set_ratio(word1.replace("_"," "),word2.replace("_"," "))/100 

    game= np.zeros(shape=(2,2))
    stream_demo=[[0.0 for y in range(50)]for x in range(len(word_list))]

    ###  GAME TEHORETIC ALGO  ###
    prob=[]
    temp=np.zeros(shape=(2,1))
    for y in range(len(word_list)):
        prob.append([[0.5],[0.5]])

    prob_rep= np.zeros(shape=(len(word_list),2))

    for i in range(50):
#         print("*********ROUND{}**********".format(i))
        for index1,word1 in enumerate(word_list):

            u1=np.zeros(shape=(2,1))
            u2=0.0
            for index2,word2 in enumerate(word_list):

                if word1!=word2:
#                     KG+ PAYOFFS
#                     game[0,0] = con[index2] * w_sim[index1][index2]* (1- fuz[index1][index2]) + con[index1]*(1-con[index2]) #+ l1*o1 + l2*(1-o1)
#                     game[0,1] = con[index1]*con[index2] +  (1-w_sim[index1][index2])*(1-con[index2])#+ l1*o1 + l2*(1-o1)
#                     game[1,0] = con[index2]* w_sim[index1][index2] * fuz[index1][index2] + (1-w_sim[index1][index2])*con[index2] + (1-con[index2])*(1-con[index1])#+ l1*(1-o1)+l2*o1
#                     game[1,1] = (1-con[index1])*con[index2] + (w_sim[index1][index2])*(1-con[index2]) #+ l1*(1-o1)+l2*o1

                    # KG PAYOFFS
                    game[0,0] = con[index2] * w_sim[index1][index2] + con[index1]*(1-con[index2]) #+ l1*o1 + l2*(1-o1)
                    game[0,1] = con[index1]*con[index2] +  (1-w_sim[index1][index2])*(1-con[index2])#+ l1*o1 + l2*(1-o1)
                    game[1,0] = (1-w_sim[index1][index2])*con[index2] + (1-con[index2])*(1-con[index1])#+ l1*(1-o1)+l2*o1
                    game[1,1] = (1-con[index1])*con[index2] + (w_sim[index1][index2])*(1-con[index2]) #+ l1*(1-o1)+l2*o1


                    temp=np.dot(game,np.asarray(prob[index2]))
                    u1 = np.add(u1,temp)
                    u2 = u2 + np.dot(np.transpose(prob[index1]),temp)[0][0]

            prob_rep[index1] = np.transpose(np.multiply(prob[index1],u1/u2))

        prob=[]
        for y in range(len(word_list)):
            prob.append([[prob_rep.tolist()[y][0]],[prob_rep.tolist()[y][1]]])
            
        for j in range(len(word_list)):
            stream_demo[j][i] = prob_rep[j,0]
 

    score=[]

    for k in range(len(word_list)):
        score.append(sum(stream_demo[k]))
    
    # weight candidates using the sum of their word scores
    for k in self.candidates.keys():
        self.weights[k] = score[word_list.index(k)]
    

