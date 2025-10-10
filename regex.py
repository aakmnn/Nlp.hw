import string

phone1 = "123-456-7890"

phone2 = "123 456 7890"

not_phone1 = "101 Howard"
def check_phone(inp):
    valid_chars = string.digits + ' -()'
    for char in inp:
        if char not in valid_chars:
            return False
    return True

assert(check_phone(phone1))
assert(check_phone(phone2))
assert(not check_phone(not_phone1))

not_phone2 = "1234"
assert(not check_phone(not_phone2))


def check_phone(inp):
    nums = string.digits
    valid_chars = nums + ' -()*'
    num_counter = 0
    for char in inp:
        if char not in valid_chars:
            return False
        if char in nums:
            num_counter += 1
    if num_counter==10:
        return True
    else:
        return False
    

assert(check_phone(phone1))
assert(check_phone(phone2))
assert(not check_phone(not_phone1))
assert(not check_phone(not_phone2))

phone3 = "123456-7890*"
assert(check_phone(phone3))

not_phone3 = "34 50 98 21 32"
not_phone4 = "34!NA5098gn#213ee2"
assert(not check_phone(not_phone3))

assert(not check_phone(not_phone4))

not_phone4 = "(34)(50)()()982132"

assert(not check_phone(not_phone3))



import re
re_punc = re.compile("([\"\''().,;:/_?!—\-])") # add spaces around punctuation
re_apos = re.compile(r"n ' t ")    # n't
re_bpos = re.compile(r" ' s ")     # 's
re_mult_space = re.compile(r"  *") # replace multiple spaces with just one

def simple_toks(sent):
    sent = re_punc.sub(r" \1 ", sent)
    sent = re_apos.sub(r" n't ", sent)
    sent = re_bpos.sub(r" 's ", sent)
    sent = re_mult_space.sub(' ', sent)
    return sent.lower().split()


text = "I don't know who Kara's new friend is-- is it 'Mr. Toad'?"
text2 = re_punc.sub(r" \1 ", text);
text3 = re_apos.sub(r" n't ", text2);
text4 = re_bpos.sub(r" 's ", text3);
re_mult_space.sub(' ', text4)

sentences = ['All this happened, more or less.',
             'The war parts, anyway, are pretty much true.',
             "One guy I knew really was shot for taking a teapot that wasn't his.",
             'Another guy I knew really did threaten to have his personal enemies killed by hired gunmen after the war.',
             'And so on.',
             "I've changed all their names."]


tokens = list(map(simple_toks, sentences))



import collections
PAD = 0; SOS = 1

def toks2ids(sentences):
    voc_cnt = collections.Counter(t for sent in sentences for t in sent)
    vocab = sorted(voc_cnt, key=voc_cnt.get, reverse=True)
    vocab.insert(PAD, "<PAD>")
    vocab.insert(SOS, "<SOS>")
    w2id = {w:i for i,w in enumerate(vocab)}
    ids = [[w2id[t] for t in sent] for sent in sentences]
    return ids, vocab, w2id, voc_cnt

ids, vocab, w2id, voc_cnt = toks2ids(tokens)

message = "😒🎦 🤢🍕"

re_frown = re.compile(r"😒|🤢")
re_frown.sub(r"😊", message)
