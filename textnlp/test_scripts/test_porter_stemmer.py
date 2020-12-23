sys.path.insert(
    1,
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
)
import porter_stemmer

def run_samples():
    """
    """
    stemmer =  porter_stemmer.PorterStemmer()

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


if __name__=="__main__":
    run_samples()
