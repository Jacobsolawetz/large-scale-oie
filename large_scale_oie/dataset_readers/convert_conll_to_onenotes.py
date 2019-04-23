import pandas as pd
import argparse
import numpy as np

#example usage
#python convert_conll_to_onenotes.py --inp extraction_conlls/test.oie.conll --domain test --out onto_notes_conlls/test2.gold_conll

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

def main(inp, domain, out):
    df = pd.read_csv(inp, sep = "\t", skip_blank_lines = False)
    df.columns = ['word_id', 'word', 'pred', 'pred_id', 'head_pred_id', 'sent_id', 'run_id', 'label']
    df['domain'] = domain
    df['part_number'] = '000'
    df['word_id'] = df['word_id'].fillna(-1)
    df['word_id'] = df['word_id'].astype(int)
    df['word_id'] = df['word_id'].astype(str)
    df['word_id'] = df['word_id'].replace('-1', np.nan)
    df['word_number'] = df['word_id']
    df['word'] = df['word']
    df['pos'] = 'XX'
    df['parse_bit'] = '-'
    df['lemma'] = '-'
    df['pred_frameset'] = '-'
    df['word_sense'] = '-'
    df['speaker'] = '-'
    df['named_entities'] = '*'
    #convert tags to OntoNotes format
    #preserve whitespace for downstream processing
    df['label'].fillna('END_SENT', inplace=True)
    tags = convert_tags(list(df['label']))
    df['tags'] = tags
    df['coref'] = '-'

    mask = df['word'].isnull()
    df = df.mask(mask)
    col_list = ['domain', 'part_number', 'word_number', 'word', 'pos', 'parse_bit', 'lemma', 'pred_frameset', 'word_sense', 'speaker', 'named_entities', 'tags', 'coref']
    df = df[col_list]
    #write to conversion document
    df.to_csv(out, sep = '\t', index = False, header = False)


def convert_tags(tags):
    onto_tags = []
    for i, item in enumerate(tags):
        if item == 'END_SENT':
            onto_tags.append('END_SENT')
            continue
        item = item.split('-')

        if item[0] == 'O':
            onto_tags.append('*')
            continue
        #start tag sequence
        if item[1] == 'B':
            if item[0] == 'P':
                onto_tag = '(V*'
            if list(item[0])[0] == 'A':
                arg_number = list(item[0])[1]
                arg = 'ARG' + arg_number
                onto_tag = '(' + arg + '*'
        #continue sequence
        if item[1] == 'I':
            onto_tag = '*'
        #if the last word, then end sequence
        if i == (len(tags) - 1):
            onto_tag += ')'
        #look ahead to end tag sequence
        next_item = tags[i+1].split('-')
        if item[0] != next_item[0]:
            #end the sequence
            onto_tag += ')'
        onto_tags.append(onto_tag)
    return onto_tags 

if __name__ == "__main__":
    print('conversion_started')
    parser = argparse.ArgumentParser(description="Convert Open IE4 extractions to CoNLL (ontonotes) format.")
    parser.add_argument("--inp", type=str, help="input file from which to read Open IE extractions.", required = True)
    parser.add_argument("--domain", type=str, help="domain to use when writing the ontonotes file.", required = True)
    parser.add_argument("--out", type=str, help="path to the output file, where CoNLL format should be written.", required = True)
    args = parser.parse_args()
    main(args.inp, args.domain, args.out)
