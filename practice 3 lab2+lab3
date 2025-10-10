#Write your own algorithms for Lemmatization#
def lemmatize(word):
    word = word.lower()
    
    # irregular dictionary
    irregulars = {
        "mice": "mouse",
        "children": "child",
        "geese": "goose",
        "went": "go",
        "done": "do",
        "better": "good",
        "worse": "bad"
    }
    if word in irregulars:
        return irregulars[word]
    
    # plural rules
    if word.endswith("ies") and len(word) > 3:
        return word[:-3] + "y"
    elif word.endswith("es") and len(word) > 2:
        return word[:-2]
    elif word.endswith("s") and len(word) > 1:
        return word[:-1]
    
    # verb forms
    if word.endswith("ing") and len(word) > 4:
        base = word[:-3]
        if base.endswith(base[-1] * 2):  # double consonant rule: running → run
            base = base[:-1]
        elif base.endswith("k"):  # like "making" → "make"
            base += "e"
        return base
    if word.endswith("ed") and len(word) > 3:
        base = word[:-2]
        if base.endswith("i"):  # studied → study
            base = base[:-1] + "y"
        elif base.endswith(base[-1] * 2):  # stopped → stop
            base = base[:-1]
        return base
    
    return word

print(lemmatize("stories"))
print(lemmatize("boxes"))
print(lemmatize("cats"))
print(lemmatize("running"))
print(lemmatize("making"))
print(lemmatize("studied"))
print(lemmatize("children"))
print(lemmatize("went"))
