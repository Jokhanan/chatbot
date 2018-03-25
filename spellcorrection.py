
# coding: utf-8

# In[20]:


import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(uInput): 
    "Most probable spelling correction for word."
    uInput_word_list = re.findall("[A-Z\-\']{2,}(?![a-z])|[A-Z\-\'][a-z\-\']+(?=[A-Z])|[\'\w\-]+",uInput)
    corrected_uinput_word_list = []
    for word in uInput_word_list:
        if len(word) > 2:
            corrected_uinput_word_list.append(max(candidates(word), key=P))
        else: 
            corrected_uinput_word_list.append(word)
    return " ".join(str(corrected_word) for corrected_word in corrected_uinput_word_list)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
