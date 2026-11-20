import sys
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF

# CONFIGURABLES ----------------------------------

# the number of slots added between each letter of the original IPA
# these slots are used for epenthesis, dipthongs, etc.
PADDING_SLOTS = 2
assert PADDING_SLOTS >= 0

# GLOBAL STATE -----------------------------------
ftr_ct = 0

# END DEFINES ------------------------------------

# NOTE ABOUT STRINGTOFEATURES
# i'm thinking of an implementation that uses a .csv file as the input/output
# of features
# that's probably pretty extensible by a user interested in conlanging; all
# they have to do to add characters, change characters, add features, or change
# features' names is to edit the spreadsheet. 
# in that case, string_to_features would involve a lookup in the spreadsheet
# features can have a value of True (+), False (-), or None (nothing in the spreadsheet)

# word: a string of IPA characters
# returns a list of features, one per parsed phoneme
# --force skips bad characters instead of erroring when
# they're encountered
def string_to_features(string: str, force=False) -> [dict]:
    empty_ftr = ({"vowel": None, "alveolar": None,},
                 {"vowel": False, "alveolar": False,}, )
    word = []
    for e in range(PADDING_SLOTS):
        word.append((dict(empty_ftr[0]), dict(empty_ftr[1])))
    ftr_ct = 2 * 2 # (2 features, * 2 for activation + existence)
    for c in string:
        if c == 'k':
            word.append(({"vowel": False, "alveolar": False,},
                         {"vowel": True, "alveolar": True,}, ))
        elif c == 'æ':
            word.append(({"vowel": True, "alveolar": None,},
                         {"vowel": True, "alveolar": False,}, ))
        elif c == 't':
            word.append(({"vowel": False, "alveolar": True,},
                         {"vowel": True, "alveolar": True,}, ))
        else:
            if force:
                pass
            else:
                raise Exception(f"unsupported input character: {c}")
        for e in range(PADDING_SLOTS):
            word.append((dict(empty_ftr[0]), dict(empty_ftr[1])))
    return word

# returns the number of the boolean variable
# that corresponds to the activation of that feature
# (the next variable will be the existence of that feature)
# pos: position in word (padding adjusted)
# f: which feature
# features: dictionary of features
def feature_to_var(features:dict, pos:int, ftr:str) -> int:
    return (len(features)*pos + features.keys().index(ftr))

# im a little worried about this function ngl.
# not every feature combination needs to correspond to a character...
# the solver could create characters that are (a) complete nonsense or (b) a
# legit character, but not quite close enough to the version in the
# spreadsheet. i need to work out a way of converting these close-enough
# feature sets, or some sort of useful feedback to the user so they can fix it.
def features_to_string(word:[tuple[dict, dict]]) -> str:
    out = ""
    for letter in word:
        if letter[1]["vowel"] is True and letter[0]["vowel"] is True:
            out += "æ"
        else:
            if letter[1]["alveolar"] is True and letter[0]["alveolar"] is True:
                out += "t"
            elif letter[1]["alveolar"] is True:
                out += "k"
    return out

# appends clauses to the supplied word, encoding the maximality faithfulness
# constraint (MAX)
def encode_MAX(word:[tuple[dict, dict]], weight:int) -> None:
    pass

# encodes the dependent / don't epenthesize faithfulness constraint (DEP)
def encode_DEP(word:[tuple[dict, dict]], weight:int) -> None:
    pass

# encodes identical faithfulness constraint (IDENT F)
# feature is the integer index of the feature in the dict
def encode_IDENT(word:[tuple[dict, dict]], feature:int, weight:int) -> None:
    pass

# -----------------------------------------------------------

if len(sys.argv) < 2:
    # "cat" in english
    word_string = "kæt"
else:
    word_string = sys.argv[1]

print(f"Input string: {word_string}")

word = string_to_features(word_string)
print(word)
print(f"Decoded string: {features_to_string(word)}")

#encoding = WCNF()

# ranking: IDENT(ALL) >> MAX >> DEP
#weight = 1
#encode_DEP(word)
#weight = 3
#encode_MAX(word)
#weight = 5

#for f in len(word[0]):
#    encode_IDENT(word, f)
