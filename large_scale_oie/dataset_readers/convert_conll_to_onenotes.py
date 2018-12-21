import pandas as pd


'''
Column Type Description
1 Document ID This is a variation on the document filename
2 Part number Some files are divided into multiple parts numbered as 000, 001, 002, ... etc.
3 Word number This is the word index in the sentence
4 Word The word itself
5 Part of Speech Part of Speech of the word
6 Parse bit This is the bracketed structure broken before the first open parenthesis in the parse, and the
word/part-of-speech leaf replaced with a *. The full parse can be created by substituting
the asterisk with the ([pos] [word]) string (or leaf) and concatenating the items in
the rows of that column.
7 Lemma The predicate/sense lemma is mentioned for the rows for which we have semantic role or
word sense information. All other rows are marked with a -
8 Predicate Frameset ID This is the PropBank frameset ID of the predicate in Column 7.
9 Word sense This is the word sense of the word in Column 4.
10 Speaker/Author This is the speaker or author name where available. Mostly in Broadcast Conversation and
Weblog data.
11 Named Entities These columns identifies the spans representing various named entities.
12:N Predicate Arguments There is one column each of predicate argument structure information for the predicate
mentioned in Column 7.
N Coreference Coreference chain information encoded in a parenthesis structure.
'''

def main():
	inp = 'extraction_conlls/test.oie.conll'
	domain = 'train'
	df = pd.read_csv(inp, sep = "\t")
	df['domain'] = domain
	df['part_number'] = 000
	df['word_number' = 'word_id'
	df[	


if __name__ == "__main__":
	print('coversion_started')
    parser = argparse.ArgumentParser(description="Convert Open IE4 extractions to CoNLL (ontonotes) format.")
    parser.add_argument("--inp", type=str, help="input file from which to read Open IE extractions.", required = True)
    parser.add_argument("--domain", type=str, help="domain to use when writing the ontonotes file.", required = True)
    parser.add_argument("--out", type=str, help="path to the output file, where CoNLL format should be written.", required = True)
    args = parser.parse_args()
    print(args.inp)
    print(args.domain)
    print(args.out)
    main(args.inp, args.domain, args.out)
