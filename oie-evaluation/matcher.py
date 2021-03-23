import string
from nltk.translate.bleu_score import sentence_bleu
from nltk.corpus import stopwords
from nltk.parse import CoreNLPParser

#parser = CoreNLPParser(url='http://localhost:9001')




class Matcher:





    @staticmethod
    def stanford_parse(sentence):
        pt = list(parser.parse(sentence))
        dl = []
        Matcher.traverse_tree(pt, 0, dl)
        if len(dl) < len(sentence):
            # TODO: there is a mismatching between parser output and raw sentence
            print('>> --- stanfordnlp bug report ---')
            print(sentence)
            print(list(parser.parse(sentence)))
            dl += (len(sentence) - len(dl)) * (dl[-1:] if len(dl) > 0 else [0])
            print('<< --- stanfordnlp bug report ---')
            assert len(dl) == len(sentence)
        elif len(dl) > len(sentence):
            raise Exception('parser longer bug')
        return dl

    def bowMatch(ref, ex, ignoreStopwords, ignoreCase):
        s1 = ref.bow()
        s2 = ex.bow()
        if ignoreCase:
            s1 = s1.lower()
            s2 = s2.lower()

        s1Words = s1.split(' ')
        s2Words = s2.split(' ')

        if ignoreStopwords:
            s1Words = Matcher.removeStopwords(s1Words)
            s2Words = Matcher.removeStopwords(s2Words)

        return sorted(s1Words) == sorted(s2Words)

    @staticmethod
    def bleuMatch(ref, ex, ignoreStopwords, ignoreCase):
        sRef = ref.bow()
        sEx = ex.bow()
        bleu = sentence_bleu(references = [sRef.split(' ')], hypothesis = sEx.split(' '))
        return bleu > Matcher.BLEU_THRESHOLD

    @staticmethod
    def syntacticHeadMatch(sentence, ref, ex, ignoreStopwords, ignoreCase):
        #working on arg syntactic head match
        #first make sure extractions agree on the predicate
        ###print(ref.args)
        ###print(ex.args)
        ###print('printing heads-----------------------')
        ###print(ref.heads)
        heads = ref.heads[1:]
        ###print(heads)

        if ex.pred not in ref.pred.split(' '):
            ###print('preds not matched')
            ###print(ref.pred + ' compared with ' + ex.pred)
            return False
        ###else:
            ###print('pred match')
            #compare args to see if the extraction is valid

        ###print(len(ref.args))
        ###print(len(ex.args))

        if len(ref.args) != len(ex.args):
            #different number of arguments extracted
            return False
        for i, head in enumerate(heads):

            #sometimes '.' is identified as the syntactic head and we do not want to count
            #these extractions as incorrect
            if head == '.':
                continue
            ###print( head + ' in ' + ex.args[i])

            if head not in ex.args[i]:
                return False

        #pt = list(parser.parse(sentence.split(' ')))
        #print(pt)
        #print(sentence)
        #sRef = ref.bow().split(' ')
        #sEx = ex.bow().split(' ')
        #count =  0
        #print([ref.elementToStr(elem) for elem in ref.args])






        #for w1 in sRef:
            #for w2 in sEx:
                #if w1 == w2:
                    #count += 1

        # We check how well does the extraction lexically cover the reference
        # Note: this is somewhat lenient as it doesn't penalize the extraction for
        #       being too long
        #coverage = float(count) / len(sRef)


        return True#coverage > Matcher.LEXICAL_THRESHOLD

    @staticmethod
    def removeStopwords(ls):
        return [w for w in ls if w.lower() not in Matcher.stopwords]

    # CONSTANTS
    BLEU_THRESHOLD = 0.4
    LEXICAL_THRESHOLD = 0.5 # Note: changing this value didn't change the ordering of the tested systems
    stopwords = stopwords.words('english') + list(string.punctuation)
