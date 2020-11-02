#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# similarity function
def similarity(w1,w2):
    try:
        sim=model_ft.similarity(w1,w2)
    except:
        sim=0.0
    return sim


# some candidate pre-processing functions

def _is_alphanum(word, valid_punctuation_marks='-'):
    """Check if a word contains only alpha-numeric
    characters and valid punctuation marks.

    """
    for punct in valid_punctuation_marks.split():
        word = word.replace(punct, '')
    return word.isalnum()

def apply_filters(phrase):
    delete=0
    count_digit=0
    min_size=3
    allowed_punctuation="\\"
    
    # delete non alphanumeric words
    if _is_alphanum(phrase)==False:
        delete=1
        
    # delete if part of stop word lists
    if phrase.lower() in stop or phrase.lower() in functional or phrase.lower() in smart_stop:
        delete=1
    
    if phrase in stop_phrase:
        delete=1
        
    # delete if word too small
    if (len(phrase)<min_size):
        delete=1
    
    # delete words which only contain digits 
    for char in phrase:
        if(char.isdigit()==True or char=='_'):
            count_digit=count_digit+1
            
        if (char.isalpha()==False and char.isdigit()==False):
            if char not in allowed_punctuation:
                delete=1
                break
    
    if count_digit==len(phrase):
        delete=1
        
    return delete

# used in candidate_selection while creating offsets
def nth_item(n, item, iterable):
    indicies = compress(count(), map(partial(eq, item), iterable))
    return next(islice(indicies, n-1, None), -1)

# numericl sort function, critical when running KG bcz topics are stored in pickle file sequentially
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


# extract top n 
def get_n_best(self,n, redundancy_removal=False, stemming=False):

    # sort candidates by descending weight
    best = sorted(self.weights, key=self.weights.get, reverse=True)

    # remove redundant candidates
    if redundancy_removal:

        # initialize a new container for non redundant candidates
        non_redundant_best = []

        # loop through the best candidates
        for candidate in best:

            # test wether candidate is redundant
            if self.is_redundant(candidate, non_redundant_best):
                continue

            # add the candidate otherwise
            non_redundant_best.append(candidate)

            # break computation if the n-best are found
            if len(non_redundant_best) >= n:
                break

        # copy non redundant candidates in best container
        best = non_redundant_best

    # lemmatize and remove lower ranked duplicates
    for i,key in enumerate(best):

        for j in range(i+1,len(best)):
            a1=[lemma.lemmatize(k) for k in best[j].split(' ')]
            k1=' '.join(a1)
            a2=[lemma.lemmatize(k) for k in key.split(' ')]
            k2=' '.join(a2)

            if k2==k1:
                del best[j]
                break

    # get the list of best candidates as (lexical form, weight) tuples
    n_best = [(u, self.weights[u]) for u in best[:min(n, len(best))]]
        
    # replace with surface forms if no stemming
    if not stemming:
        n_best = [(' '.join(self.candidates[u].surface_forms[0]).lower(),
                   self.weights[u]) for u in best[:min(n, len(best))]]

    if len(n_best) < n:
        logging.warning(
            'Not enough candidates to choose from '
            '({} requested, {} given)'.format(n, len(n_best)))

    # return the list of best candidates
    return n_best

