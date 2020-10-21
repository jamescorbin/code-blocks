vowels = ('a', 'e', 'i', 'o', 'u')
'''
    Docstrings explaining the algorithm are taken directly
    from the original literature.

    Code is written the interpretation of that text
    by J. Corbin.
'''

###############################################################################

###############################################################################

def is_vowel(char, prev_char=''):
    '''
    parameters:
        -- char, character in question
        -- prev_char, (optional) previous character. See desc. on 'y'
    returns:
        -- boolean

    A \consonant\ in a word is a letter other than A, E, I, O or U, and other
    than Y preceded by a consonant. (The fact that the term `consonant' is
    defined to some extent in terms of itself does not make it ambiguous.) So in
    TOY the consonants are T and Y, and in SYZYGY they are S, Z and G. If a
    letter is not a consonant it is a \vowel\.

    A consonant will be denoted by c, a vowel by v. A list ccc... of length
    greater than 0 will be denoted by C, and a list vvv... of length greater
    than 0 will be denoted by V. Any word, or part of a word, therefore has one
    of the four forms:

        CVCV ... C
        CVCV ... V
        VCVC ... C
        VCVC ... V

    These may all be represented by the single form

        [C]VCVC ... [V]
    '''
    return ((char in vowels) or
            (char=='y' and (not prev_char in vowels and prev_char!='')))

###############################################################################

###############################################################################

def is_const(char, prev_char=''):
    '''
        c.f. is_vowel()
    '''
    return ~is_vowel(char, prev_char)

###############################################################################

###############################################################################

has_vowel = lambda word: any(
                    [is_vowel(char, word[i-1]) if i>0 else is_vowel(char)
                    for i, char in enumerate(word)])
final_double_const = lambda word: word[-2]==word[-1] and not is_vowel(word[-1])

###############################################################################

###############################################################################

def cvc_form(word):
    '''
    parameters:
        -- word, a string
    returns:
        -- boolean, whether cvc form

    A consonant will be denoted by c, a vowel by v. A list ccc... of length
    greater than 0 will be denoted by C, and a list vvv... of length greater
    than 0 will be denoted by V. Any word, or part of a word, therefore has one
    of the four forms:

        CVCV ... C
        CVCV ... V
        VCVC ... C
        VCVC ... V
    '''
    return_val = False
    if len(word) >= 3:
        vowel_check = [is_vowel(char, word[i-1]) if i>0
		else is_vowel(char) for i, char in enumerate(word)]
    if (~vowel_check[0]) and (~vowel_check[-1]):
        num_changes = 0
        for i in range(len(word) - 1):
            if vowel_check[i] != vowel_check[i+1]:
                num_changes += 1
        if num_changes == 2:
            return_val = True
    return return_val

###############################################################################

###############################################################################

def const_vowel_m(word):
    '''
    parameters:
        -- word, a string
    returns:
        -- m, an int

    These may all be represented by the single form

        [C]VCVC ... [V]

    where the square brackets denote arbitrary presence of their contents.
    Using (VC){m} to denote VC repeated m times, this may again be written as

        [C](VC){m}[V].

    m will be called the \measure\ of any word or word part when represented in
    this form. The case m = 0 covers the null word. Here are some examples:

        m=0    TR,  EE,  TREE,  Y,  BY.
        m=1    TROUBLE,  OATS,  TREES,  IVY.
        m=2    TROUBLES,  PRIVATE,  OATEN,  ORRERY.

    The \rules\ for removing a suffix will be given in the form

        (condition) S1 -> S2

    This means that if a word ends with the suffix S1, and the stem before S1
    satisfies the given condition, S1 is replaced by S2. The condition is
    usually given in terms of m, e.g.

        (m > 1) EMENT ->

    Here S1 is `EMENT' and S2 is null. This would map REPLACEMENT to REPLAC,
    since REPLAC is a word part for which m = 2.

    The `condition' part may also contain the following:

    *S  - the stem ends with S (and similarly for the other letters).

    *v* - the stem contains a vowel.

    *d  - the stem ends with a double consonant (e.g. -TT, -SS).

    *o  - the stem ends cvc, where the second c is not W, X or Y (e.g.
           -WIL, -HOP).

    And the condition part may also contain expressions with \and\, \or\ and
    \not\, so that

        (m>1 and (*S or *T))

    tests for a stem with m>1 ending in S or T, while

        (*d and not (*L or *S or *Z))

    tests for a stem ending witha double consonant other than L, S or Z.
    Elaborate conditions like this are required only rarely.
    '''
    vowel_check = [is_vowel(char, word[i-1]) if i>0
		else is_vowel(char) for i, char in enumerate(word)]

    if any(vowel_check):
        start_vowel_ind = vowel_check.index(True)
    else:
        start_vowel_ind = len(word)
    if not all(vowel_check):
        final_const_ind = (len(vowel_check)
                           - vowel_check[::-1].index(False) - 1)
    else:
        final_const_ind = -1

    if final_const_ind - start_vowel_ind > 0:
        vowel_check = vowel_check[start_vowel_ind:final_const_ind+1]
        num_changes = 0
        for i in range(len(vowel_check) - 1):
            if vowel_check[i] != vowel_check[i+1]:
                num_changes += 1
        m = (num_changes + 1)//2
    else:
        m = 0

    return m

###############################################################################

###############################################################################

class PorterStemmer():

    ###########################################################################
    '''
    The step_\d_map attribute is encoded
    from the literature.
    See the step_\d methods for a quote of the text.
    '''
    step_2_map = {
                    'ational': 'ate',
                    'tional': 'tion',
                    'enci': 'ence',
                    'anci': 'ance',
                    'izer': 'ize',
                    'abli': 'able',
                    'alli': 'al',
                    'entli': 'ent',
                    'eli': 'e',
                    'ousli': 'ous',
                    'ization': 'ize',
                    'ation': 'ate',
                    'ator': 'ate',
                    'alism': 'al',
                    'iveness': 'ive',
                    'fulness': 'ful',
                    'ousness': 'ous',
                    'aliti': 'al',
                    'iviti': 'ive',
                    'biliti': 'ble',
                    }
    step_3_map = {
                    'icate': 'ic',
                    'ative': '',
                    'alize': 'al',
                    'iciti': 'ic',
                    'ical': 'ic',
                    'ful': '',
                    'ness': '',
                    }
    step_4_map = {
                    'al': '',
                    'ance': '',
                    'ence': '',
                    'er': '',
                    'ic': '',
                    'able': '',
                    'ible': '',
                    'ant': '',
                    'ement': '',
                    'ment': '',
                    'ent': '',
                    'ou': '',
                    'ism': '',
                    'ate': '',
                    'iti': '',
                    'ous': '',
                    'ive': '',
                    'ize': '',
                    }

    ###########################################################################

    ###########################################################################

    def __init__(self):

        pass

    ###########################################################################

    ###########################################################################

    def run_word(self, word):
        '''
        parameters:
            -- word, a string; the word to be stemmed
        returns:
            -- word, a string; the stemmed word
        '''
        word = self.custom_step(word)
        word = self.step_1(word)
        word = self.step_2(word)
        word = self.step_3(word)
        word = self.step_4(word)
        word = self.step_5(word)

        return word

    ###########################################################################

    ###########################################################################

    def run(self, words):
        '''
        parameters:
            -- words, list of strings
        returns:
            -- words, stemmed list of words
        '''
        for i, word in enumerate(words):
            words[i] = self.run_word(word)
        return words

    ###########################################################################

    ###########################################################################

    def custom_step(self, word):

        new_word = word
        if word[-5:] == "ingly":
            new_word = word[:-2]
        elif word[-3:] == "ist":
            if const_vowel_m(word[:-3]) >= 2:
                new_word = word[:-3]
        return new_word

    ###########################################################################

    ###########################################################################

    def step_1(self, word):
        '''
        parameters:
            -- word, a string; the word to be stemmed

        In a set of rules written beneath each other, only one is obeyed, and this
        will be the one with the longest matching S1 for the given word. For
        example, with

            SSES -> SS
            IES  -> I
            SS   -> SS
            S    ->

        (here the conditions are all null) CARESSES maps to CARESS since SSES is
        the longest match for S1. Equally CARESS maps to CARESS (S1=`SS') and CARES
        to CARE (S1=`S').

        In the rules below, examples of their application, successful or otherwise,
        are given on the right in lower case. The algorithm now follows:

        Step 1a

            SSES -> SS                         caresses  ->  caress
            IES  -> I                          ponies    ->  poni
                                               ties      ->  ti
            SS   -> SS                         caress    ->  caress
            S    ->                            cats      ->  cat

        Step 1b

            (m>0) EED -> EE                    feed      ->  feed
                                               agreed    ->  agree
            (*v*) ED  ->                       plastered ->  plaster
                                               bled      ->  bled
            (*v*) ING ->                       motoring  ->  motor
                                               sing      ->  sing

        If the second or third of the rules in Step 1b is successful, the following
        is done:

            AT -> ATE                       conflat(ed)  ->  conflate
            BL -> BLE                       troubl(ed)   ->  trouble
            IZ -> IZE                       siz(ed)      ->  size
            (*d and not (*L or *S or *Z))
               -> single letter
                                            hopp(ing)    ->  hop
                                            tann(ed)     ->  tan
                                            fall(ing)    ->  fall
                                            hiss(ing)    ->  hiss
                                            fizz(ed)     ->  fizz
            (m=1 and *o) -> E               fail(ing)    ->  fail
                                            fil(ing)     ->  file

        The rule to map to a single letter causes the removal of one of the double
        letter pair. The -E is put back on -AT, -BL and -IZ, so that the suffixes
        -ATE, -BLE and -IZE can be recognised later. This E may be removed in step
        4.

        Step 1c

            (*v*) Y -> I                    happy        ->  happi
                                            sky          ->  sky

        Step 1 deals with plurals and past participles. The subsequent steps are
        much more straightforward.
        '''
        new_word = word
        extra_cond = False

        if new_word[-4:]=='sses':
            new_word = new_word[:-4] + 'ss'
        elif new_word[-3:]=='ies':
            new_word = new_word[:-3]+'i'
        elif new_word[-2:]!='ss' and new_word[-1]=='s':
            new_word = new_word[:-1]

        if (new_word[-3:]=='eed'):
            if const_vowel_m(new_word[:-3]) > 0:
                new_word = new_word[:-3]+'ee'
        elif (new_word[-2:]=='ed'):
            if has_vowel(new_word[:-2]):
                new_word = new_word[:-2]
                extra_cond = True
        elif ((new_word[-3:]=="ing")
                and has_vowel(new_word[:-3])):
            new_word = new_word[:-3]
            extra_cond = True

        if extra_cond:
            if ((new_word[-2:]=='at')
                    or (new_word[-2:]=='bl')
                    or (new_word[-2:]=='iz')):
                new_word = new_word + 'e'
            elif ((new_word[-1] not in ('l', 's', 'z'))
                        and final_double_const(new_word)):
                new_word = new_word[:-1]
            elif ((const_vowel_m(new_word)==1)
                  and len(new_word) >= 3
                  and cvc_form(new_word[-3:])):
                new_word = new_word + 'e'

        if new_word[-1]=='y' and has_vowel(new_word[:-1]):
            new_word = new_word[:-1] + 'i'

        return new_word

    ###########################################################################

    ###########################################################################

    def step_2(self, word):
        '''
        parameters:
            -- word, a string; word to be stemmed.
        returns:
            -- word, a string; the stemmed word.

        Step 2

            (m>0) ATIONAL ->  ATE           relational     ->  relate
            (m>0) TIONAL  ->  TION          conditional    ->  condition
                                            rational       ->  rational
            (m>0) ENCI    ->  ENCE          valenci        ->  valence
            (m>0) ANCI    ->  ANCE          hesitanci      ->  hesitance
            (m>0) IZER    ->  IZE           digitizer      ->  digitize
            (m>0) ABLI    ->  ABLE          conformabli    ->  conformable
            (m>0) ALLI    ->  AL            radicalli      ->  radical
            (m>0) ENTLI   ->  ENT           differentli    ->  different
            (m>0) ELI     ->  E             vileli        - >  vile
            (m>0) OUSLI   ->  OUS           analogousli    ->  analogous
            (m>0) IZATION ->  IZE           vietnamization ->  vietnamize
            (m>0) ATION   ->  ATE           predication    ->  predicate
            (m>0) ATOR    ->  ATE           operator       ->  operate
            (m>0) ALISM   ->  AL            feudalism      ->  feudal
            (m>0) IVENESS ->  IVE           decisiveness   ->  decisive
            (m>0) FULNESS ->  FUL           hopefulness    ->  hopeful
            (m>0) OUSNESS ->  OUS           callousness    ->  callous
            (m>0) ALITI   ->  AL            formaliti      ->  formal
            (m>0) IVITI   ->  IVE           sensitiviti    ->  sensitive
            (m>0) BILITI  ->  BLE           sensibiliti    ->  sensible

        The test for the string S1 can be made fast by doing a program switch on
        the penultimate letter of the word being tested. This gives a fairly even
        breakdown of the possible values of the string S1. It will be seen in fact
        that the S1-strings in step 2 are presented here in the alphabetical order
        of their penultimate letter. Similar techniques may be applied in the other
        steps.
        '''
        return self.steps_234_template(word, self.step_2_map, 1)

    ###########################################################################

    ###########################################################################

    def step_3(self, word):
        '''
        parameters:
            -- word, a string; word to be stemmed.
        returns:
            -- word, a string; the stemmed word.

        Step 3

            (m>0) ICATE ->  IC              triplicate     ->  triplic
            (m>0) ATIVE ->                  formative      ->  form
            (m>0) ALIZE ->  AL              formalize      ->  formal
            (m>0) ICITI ->  IC              electriciti    ->  electric
            (m>0) ICAL  ->  IC              electrical     ->  electric
            (m>0) FUL   ->                  hopeful        ->  hope
            (m>0) NESS  ->                  goodness       ->  good
        '''
        return self.steps_234_template(word, self.step_3_map, 1)

    ###########################################################################

    ###########################################################################

    def step_4(self, word):
        '''
        parameters:
            -- word, a string; word to be stemmed.
        returns:
            -- word, a string; the stemmed word.

        Step 4

            (m>1) AL    ->                  revival        ->  reviv
            (m>1) ANCE  ->                  allowance      ->  allow
            (m>1) ENCE  ->                  inference      ->  infer
            (m>1) ER    ->                  airliner       ->  airlin
            (m>1) IC    ->                  gyroscopic     ->  gyroscop
            (m>1) ABLE  ->                  adjustable     ->  adjust
            (m>1) IBLE  ->                  defensible     ->  defens
            (m>1) ANT   ->                  irritant       ->  irrit
            (m>1) EMENT ->                  replacement    ->  replac
            (m>1) MENT  ->                  adjustment     ->  adjust
            (m>1) ENT   ->                  dependent      ->  depend
            (m>1 and (*S or *T)) ION ->     adoption       ->  adopt
            (m>1) OU    ->                  homologou      ->  homolog
            (m>1) ISM   ->                  communism      ->  commun
            (m>1) ATE   ->                  activate       ->  activ
            (m>1) ITI   ->                  angulariti     ->  angular
            (m>1) OUS   ->                  homologous     ->  homolog
            (m>1) IVE   ->                  effective      ->  effect
            (m>1) IZE   ->                  bowdlerize     ->  bowdler

        The suffixes are now removed. All that remains is a little tidying up.
        '''
        new_word = word
        if word[-4:] == "sion" or word[-4:] == "tion":
            if const_vowel_m(word[:-3]) >= 2:
                new_word = word[:-3]
        else:
            new_word = self.steps_234_template(word, self.step_4_map, 2)
        return new_word

    ###########################################################################

    ###########################################################################

    def step_5(self, word):
        '''
        parameters:
            -- word, a string; word to be stemmed.
        returns:
            -- word, a string; the stemmed word.

        Step 5a

            (m>1) E     ->                  probate        ->  probat
                                            rate           ->  rate
            (m=1 and not *o) E ->           cease          ->  ceas

        Step 5b

            (m > 1 and *d and *L) -> single letter
                                            controll       ->  control
                                            roll           ->  roll
        '''
        new_word = word
        if (new_word[-1] == 'e') and (const_vowel_m(new_word[:-1])>1):
            new_word = new_word[:-1]
        elif ((new_word[-1] == 'e') and (const_vowel_m(new_word[:-1])==1)
                and
                ((len(new_word) < 4) or not cvc_form(new_word[-4:-1]))
                ):
            new_word = new_word[:-1]

        if ((len(new_word)>1)
                and (new_word[-1]=='l')
                and (new_word[-1]==new_word[-2])
                and (const_vowel_m(new_word)>1)
                ):
            new_word = new_word[:-1]

        return new_word

    ###########################################################################

    ###########################################################################

    def steps_234_template(self, word, mapping, m_bounds):

        new_word = word
        stop = False
        for k, v in mapping.items():
            if ((not stop)
                    and (len(word) >= len(k))
                    and (word[-len(k):]==k)
                    and (const_vowel_m(word[:-len(k)]) >= m_bounds)):
                new_word = word[:-len(k)] + v
                stop = True
        return new_word

    ###########################################################################

###############################################################################

###############################################################################

def run_samples():

    stemmer =  PorterStemmer()

    words_1 = [
            ("caresses", "caress"),
            ("ponies", "poni"),
            ("ties", "ti"),
            ("caress", "caress"),
            ("cats", "cat"),
            ("feed", "feed"),
            ("agreed", "agree"),
            ("plastered", "plaster"),
            ("bled", "bled"),
            ("motoring", "motor"),
            ("sing", "sing"),
            ("conflated", "conflate"),
            ("troubled", "trouble"),
            ("sized", "size"),
            ("hopping", "hop"),
            ("tanned", "tan"),
            ("falling", "fall"),
            ("hissing", "hiss"),
            ("fizzed", "fizz"),
            ("failing", "fail"),
            ("filing", "file"),
            ("happy", "happi"),
            ("sky", "sky"),
            ]
    words_2 = [
            ("relational", "relate"),
            ("conditional", "condition"),
            ("rational", "rational"),
            ("valenci", "valence"),
            ("hesitanci", "hesitance"),
            ("digitizer", "digitize"),
            ("conformabli", "conformable"),
            ("radicalli", "radical"),
            ("differentli", "different"),
            ("vileli", "vile"),
            ("analogousli", "analogous"),
            ("vietnamization", "vietnamize"),
            ("predication", "predicate"),
            ("operator", "operate"),
            ("feudalism", "feudal"),
            ("decisiveness", "decisive"),
            ("hopefulness", "hopeful"),
            ("callousness", "callous"),
            ("formaliti", "formal"),
            ("sensitiviti", "sensitive"),
            ("sensibiliti", "sensible"),
            ]
    words_3 = [
            ("triplicate", "triplic"),
            ("formative", "form"),
            ("formalize", "formal"),
            ("electriciti", "electric"),
            ("electrical", "electric"),
            ("hopeful", "hope"),
            ("goodness", "good"),
            ]
    words_4 = [
            ("revival", "reviv"),
            ("allowance", "allow"),
            ("inference", "infer"),
            ("airliner", "airlin"),
            ("gyroscopic", "gyroscop"),
            ("adjustable", "adjust"),
            ("defensible", "defens"),
            ("irritant", "irrit"),
            ("replacement", "replac"),
            ("adjustment", "adjust"),
            ("dependent", "depend"),
            ("adoption", "adopt"),
            ("homologou", "homolog"),
            ("communism", "commun"),
            ("activate", "activ"),
            ("angulariti", "angular"),
            ("homologous", "homolog"),
            ("effective", "effect"),
            ("bowdlerize", "bowdler"),
            ]
    words_5 = [
            ("probate", "probat"),
            ("rate", "rate"),
            ("cease", "ceas"),
            ("controll", "control"),
            ("roll", "roll"),
            ]

    for w1, w2 in words_1:
        print(w1, w2, stemmer.step_1(w1))
    for w1, w2 in words_2:
        print(w1, w2, stemmer.step_2(w1))
    for w1, w2 in words_3:
        print(w1, w2, stemmer.step_3(w1))
    for w1, w2 in words_4:
        print(w1, w2, stemmer.step_4(w1))
    for w1, w2 in words_5:
        print(w1, w2, stemmer.step_5(w1))

###############################################################################

###############################################################################

if __name__=="__main__":
    import argparse
    import re
    parser = argparse.ArgumentParser(
            description="Counts unique words in Project Gutenburg text.")
    parser.add_argument("--file_names", nargs="+", help='')
    args = parser.parse_args()

    file_names = args.file_names
    stemmer =  PorterStemmer()

    for fn in file_names:
        with open(fn, 'r') as f:
            words = [x.strip() for x in f]
        words = stemmer.run(words)
        with open(fn, 'w') as f:
            f.write('\n'.join(words))
