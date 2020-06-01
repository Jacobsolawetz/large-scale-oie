#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 12:30:22 2018

@author: jacobsolawetz


Code to convert the large scale QA-SRL dataset to open information extraction Conll format.  
"""

import codecs
import os
import logging
from typing import Dict, List, Optional, Tuple
from collections import Counter
import json
import gzip
from oie_readers.extraction import Extraction, escape_special_chars, normalize_element
import re
import itertools
from fuzzywuzzy import process
from fuzzywuzzy.utils import full_process
from fuzzywuzzy.string_processing import StringProcessor
from fuzzywuzzy.utils import asciidammit
from operator import itemgetter
import pdb


import sys
reload(sys)
sys.setdefaultencoding("utf-8")




QUESTION_TRG_INDEX =  3 # index of the predicate within the question
QUESTION_MODALITY_INDEX = 1 # index of the modality within the question


PASS_ALL = lambda x: x
MASK_ALL = lambda x: "_"
get_default_mask = lambda : [PASS_ALL] * 8
# QA-SRL vocabulary for "AUX" placement, which modifies the predicates
QA_SRL_AUX_MODIFIERS = [
 #   "are",
    "are n't",
    "can",
    "ca n't",
    "could",
    "could n't",
#    "did",
    "did n't",
#    "do",
#    "does",
    "does n't",
    "do n't",
    "had",
    "had n't",
#    "has",
    "has n't",
#    "have",
    "have n't",
#    "is",
    "is n't",
    "may",
    "may not",
    "might",
    "might not",
    "must",
    "must n't",
    "should",
    "should n't",
#    "was",
    "was n't",
#    "were",
    "were n't",
    "will",
    "wo n't",
    "would",
    "would n't",
]







class QASRL_extractor():

#useful link
#https://github.com/nafitzgerald/nrl-qasrl/blob/master/nrl/data/dataset_readers/qasrl_reader.py

##a helper class to read the new QA-SRL data format 
    def __init__(self, qa_path, output_file, dist_file, write, length, sort, output_eval, min_correct = 5/(6 * 1.0)):
        self.dist_file = dist_file
        self.qa_path = qa_path
        self.output_file = output_file
        self.min_correct = min_correct
        #for the creation of question dist
        self.extractions = []
        self.write = write
        self.sort = sort
        self.length = length
        self.output_eval = output_eval

    def read(self):
        ###What to do about generalized questions that are not yet in this distribution set?####
        ###Use analyze.py####
        question_dist = dict([(q, dict([(int(loc), cnt)
                                             for (loc, cnt)
                                             in dist.iteritems()]))
                                   for (q, dist)
                                   in json.load(open(self.dist_file)).iteritems()]) \
                                       if self.dist_file\
                                          else {}
        ##pull sentence##
        ##pull predicate##
        ##pull qa pairs with 5/6 or more validations##
        ##possibly preprocess at this step##
        #load json lines data into list
        qa_path = self.qa_path
        data = []
        with codecs.open(qa_path, 'r', encoding='utf8') as f:
            for line in f:
                data.append(json.loads(line))


        f_out = open(self.output_file, "w")
        jsonl_out = open('science_eval_sent.jsonl',"w")
        eval_out = open('science_eval.oie',"w")
        verb_types = []
        #parse qa data
        for item in data:
        #for item in data[(len(data)-100):(len(data) - 1)]:
            sent_id = item["sentenceId"].encode('utf-8')
            #remove science
            if sent_id.split(':')[0] != 'TQA':
                continue
            sentence_tokens = item["sentenceTokens"]
            sentence = ' '.join(sentence_tokens)
            sentence = sentence.encode('utf-8')
            if output_eval:
                jsonl_out.write("{" + '"' + "sentence" + '"' + ": " + '"' +  sentence + '"' + "}" + '\n')

            for _, verb_entry in item["verbEntries"].items():
                verb_index = verb_entry["verbIndex"]
                verb_inflected_forms = verb_entry["verbInflectedForms"]
                base_pred = sentence_tokens[verb_index]
                surfacePred = base_pred
                answer_list = []
                questions = []

                for _, question_label in verb_entry["questionLabels"].items():
                    #print(question_label["answerJudgments"])
                    answers = len(question_label["answerJudgments"])
                    valid_answers = len([ans for ans in question_label["answerJudgments"] if ans["isValid"]])
                    if valid_answers/(answers* 1.0)  < self.min_correct:
                        #do not log this question set
                        continue
                    q_string = question_label['questionString']
                    ans_spans = []
                    for ans in question_label["answerJudgments"]:
                        if ans["isValid"]:
                            for span in ans["spans"]:
                                ans_spans.append(span)
                    #add long/short flag here
                    consolidated_spans = consolidate_answers(ans_spans, self.length)
                    #look up answers in sentence tokens
                    lookup_ans = lambda ans, sentence: ' '.join(sentence[ans[0]:ans[1]])
                    consolidated_ans = map(lookup_ans, consolidated_spans, [sentence_tokens]*len(consolidated_spans))
                    #here we can acquire of the question slots
                    wh = question_label["questionSlots"]["wh"].split()
                    wh = '_'.join(wh)
                    aux = question_label["questionSlots"]["aux"].split()
                    aux = '_'.join(aux)
                    subj = question_label["questionSlots"]["subj"].split()
                    subj = '_'.join(subj)
                    #iterate through and check verb types for len > 2
                    verb_type = question_label['questionSlots']['verb']
                    inflected_verb = verb_inflected_forms[verb_type.split()[-1]]
                    if len(verb_type.split()) == 1:
                        trg =  inflected_verb
                    else:
                        trg = verb_type.split()[:-1]
                        trg.append(inflected_verb)
                        trg = "_".join(trg)
                    obj1 = question_label["questionSlots"]["obj"].split()
                    obj1 = '_'.join(obj1)
                    pp = question_label["questionSlots"]["prep"].split()
                    pp = '_'.join(pp)
                    obj2 = question_label["questionSlots"]["obj2"].split()
                    obj2 = '_'.join(obj2)

                    slotted_q = " ".join((wh,aux,subj,trg,obj1,pp,obj2,"?"))

                    curSurfacePred = augment_pred_with_question(base_pred, slotted_q)
                    if len(curSurfacePred) > len(surfacePred):
                        surfacePred = curSurfacePred

                    questions.append(slotted_q)
                    answer_list.append(consolidated_ans)
                    #print wh, subj, obj1
                    #for ans in consolidated_spans:
                        #question_answer_pairs.append((slotted_q,' '.join(sentence_tokens[ans[0]:ans[1]])))

                    ####this needs to be more sophisticated
                    ###for each predicate - create a list of qa pairs, s.t. each unique combination of questions and answers appear
                    ### e.g. 2 quesions each with 2 answers, leads to four qa pairs ((q1,a1),(q2,a1), ((q1,a1),(q2,a2)), ect.
                    ### each one of these sets will lead to an extraction

                    #now we have the augmented Pred with aux
                    #might want to revisit this methodology

                    #augment verb with aux
# =============================================================================
#                     if aux in QA_SRL_AUX_MODIFIERS:
#                         
#                         if len(verb_type.split()) == 1:
#                                 verb = aux + " " + inflected_verb
#                                 
#                         else:
#                             #add the first modifier in verb tpye
#                             #may need to revisit - in previous approach, it looks like only the surface verb and aux were sent
#                             verb = aux + " " + verb_type.split()[0] + " " + inflected_verb
#                         
#                     else:
#                         if len(verb_type.split()) == 1:
#                                 verb = inflected_verb
#                                 
#                         else:
#                             verb = verb_type.split()[0] + " " + inflected_verb
#                     
# =============================================================================
                    ##now we have sentence tokens, verb index, valid question, valid answer spans
                    ##need question blanks for augement pred with question 
                ###for each predicate - create a list of qa pairs, s.t. each unique combination of questions and answers appear
                ### e.g. 2 quesions each with 2 answers, leads to four qa pairs ((q1,a1),(q2,a1)), ((q1,a1),(q2,a2)), ect.
                ### each one of these sets will lead to an extraction                
                ##noticing many instances where the rare answer doesn't make sense
                ##e.g. Clouds that form on the ground are called fog

                ##what about questions that encode a similar argument? e.g. what for and why
                ##These organisms need the oxygen plants release to get energy out of the food .
                #[(u'what _ _ needs something _ _ ?', u'organisms'), (u'why does something need something _ _ ?', u'to get energy out of the food'), (u'what does something need _ _ _ ?', u'oxygen'), (u'what does someone need something for _ ?', u'to get energy out of the food')]
                #need    need    organisms       oxygen  for to get energy out of the food       to get energy out of the food
                #Considering the following edits - for each argument, only take the first question that appears for it
                #Considering the following edits - Only consider an answer span if it apoears by more than one annotator. Rare answers tend to be misleading
                surfacePred = surfacePred.encode('utf-8')
                base_pred = base_pred.encode('utf-8')
                #pred_indices = all_index(sentence, base_pred, matchCase = False)
                augmented_pred_indices = fuzzy_match_phrase(surfacePred.split(" "),
                                                               sentence.split(" "))
                #print augmented_pred_indices
                if not augmented_pred_indices:
                    #find equivalent of pred_index
                    head_pred_index = [verb_index]

                else:
                    head_pred_index = augmented_pred_indices[0]
                for ans_set in list(itertools.product(*answer_list)):
                    cur = Extraction((surfacePred, [head_pred_index]), 
                                 verb_index,
                                 sentence,
                                 confidence = 1.0,
                                 question_dist = self.dist_file
                                 )
                    #print 'Extraction', (surfacePred, [head_pred_index]), verb_index, sentence
                    q_as = zip(questions,ans_set)
                    if len(q_as) == 0:
                        continue
                    for q_a in q_as:
                        q = q_a[0].encode('utf-8')
                        a = q_a[1].encode('utf-8')
                        preproc_arg = self.preproc(a)
                        if not preproc_arg:
                            logging.warn("Argument reduced to None: {}".format(a))
                        indices = fuzzy_match_phrase(preproc_arg.split(" "),
                                                 sentence.split(" "))
                        #print 'q', q, 'preproc arg', preproc_arg, 'indices ', indices
                        cur.addArg((preproc_arg,indices),q)

                    if cur.noPronounArgs():

                        #print 'arguments', (preproc_arg,indices), q
                        cur.resolveAmbiguity()
                        if self.write:
                            #print sentence
                            #print q_as
                            if self.sort:
                                cur.getSortedArgs()
                            #print(cur.conll(external_feats = [1,2]))
                            f_out.write(cur.conll(external_feats = [1,2]))
                            f_out.write('\n')
                        ### now to get the ordering down
                        ### seems like now and from before, the arguments are in the order they appear in the qa file... 
                        ### get sent and word ID
                        ### generating an output file for downstream evaluation on OIE-2016
                        ### evaluation framework
                        if self.output_eval:
                            if self.sort:
                                cur.getSortedArgs()
                            eval_out.write(sentence + ' \t' + cur.__str__() + '\n')

                        self.extractions.append(cur)
                       # print cur.noPronounArgs()
                    #print q_as
                    #print cur.__str__()

#                print 'pred ', surfacePred
#                print 'pred indices ', pred_indices
#                print 'sentence ', sentence

    def preproc(self, s):
        """
        Returns a unified preproc of a string:
          - Removes duplicates spaces, to allow for space delimited words.
        """
        return " ".join([w for w in s.split(" ") if w])


def consolidate_answers(answers, length):
    """
    #########Deprecated: this method now returns the longest span in order to capture information lost from
    truncating to the shortest span.

    Returns the shortest or the longest span among options

    For a given list of answers, returns only minimal answers - e.g., ones which do not
    contain any other answer in the set.
    This deals with certain QA-SRL anntoations which include a longer span than that is needed.
    """
    '''
    Does also require that each answer overlap with at least one other valid answer in order to remove errant answers
    '''
    ret = []
    if length == 'short':
        for i, span1 in enumerate(answers):
            includeFlag = True
            overlapFlag = False
            if span1 in ret:
                includeFlag = False
                continue
            for j, span2 in enumerate(answers):
                if (i != j):
                    if span1 != span2:
                        if range(span2[0],span2[1])[0] in range(span1[0],span1[1]) and range(span2[0],span2[1])[-1] in range(span1[0],span1[1]):
                            includeFlag = False
                    if range(span1[0],span1[1])[0] in range(span2[0],span2[1]) or range(span1[0],span1[1])[-1] in range(span2[0],span2[1]):
                         overlapFlag = True
            if includeFlag and overlapFlag:
                ret.append(span1)
    else:
        for i, span1 in enumerate(answers):
            includeFlag = True
            overlapFlag = False
            if span1 in ret:
                includeFlag = False
                continue
            for j, span2 in enumerate(answers):
                if (i !=j):
                    if span1 != span2:
                        if range(span1[0], span1[1])[0] in range(span2[0],span2[1]) and range(span1[0],span1[1])[-1] in range(span2[0],span2[1]):
                            #the candidate span is then contained in another
                            includeFlag = False
                    if range(span1[0],span1[1])[0] in range(span2[0],span2[1]) or range(span1[0],span1[1])[-1] in range(span2[0],span2[1]):
                        #then the candidate span overlaps with at least one other
                        overlapFlag = True
            if includeFlag and overlapFlag:
                ret.append(span1)

    return ret


def all_index(s, ss, matchCase = True, ignoreSpaces = True):
    ''' find all occurrences of substring ss in s '''
    if not matchCase:
        s = s.lower()
        ss = ss.lower()
    if ignoreSpaces:
        s = s.replace(' ', '')
        ss = ss.replace(' ','')
    return [m.start() for m in re.finditer(re.escape(ss), s)]



def augment_pred_with_question(pred, question):
    """
    Decide what elements from the question to incorporate in the given
    corresponding predicate
    """
    # Parse question
    wh, aux, sbj, trg, obj1, pp, obj2 = map(normalize_element,
                                            question.split(' ')[:-1]) # Last split is the question mark

    # Add auxiliary to the predicate
    if aux in QA_SRL_AUX_MODIFIERS:
        return " ".join([aux, pred])

    # Non modified predicates
    return pred

def fuzzy_match_phrase(phrase, sentence):
    """
    Fuzzy find the indexes of all word in phrase against a given sentence (both are lists of words),
    returns a list of indexes in the length of phrase which match the best return from fuzzy.
    """
    logging.debug("Fuzzy searching \"{}\" in \"{}\"".format(" ".join(phrase), " ".join(sentence)))
    limit = min((len(phrase) / 2) + 1, 3)
    possible_indices = [fuzzy_match_word(w,
                                         sentence,
                                         limit) \
                        + (fuzzy_match_word("not",
                                           sentence,
                                           limit) \
                           if w == "n't" \
                           else [])
                        for w in phrase]
    indices = find_consecutive_combinations(*possible_indices)
    if not indices:
        logging.debug("\t".join(map(str, ["*** {}".format(len(indices)),
                                          " ".join(phrase),
                                          " ".join(sentence),
                                          possible_indices,
                                          indices])))
    return indices


def find_consecutive_combinations(*lists):
    """
    Given a list of lists of integers, find only the consecutive options from the Cartesian product.
    """
    ret = []
    desired_length = len(lists) # this is the length of a valid walk
    logging.debug("desired length: {}".format(desired_length))
    for first_item in lists[0]:
        logging.debug("starting with {}".format(first_item))
        cur_walk = [first_item]
        cur_item = first_item
        for ls_ind, ls in enumerate(lists[1:]):
            logging.debug("ls = {}".format(ls))
            for cur_candidate in ls:
                if cur_candidate - cur_item == 1:
                    logging.debug("Found match: {}".format(cur_candidate))
                    # This is a valid option from this list,
                    # add it and break out of this list
                    cur_walk.append(cur_candidate)
                    cur_item = cur_candidate
                    break
            if len(cur_walk) != ls_ind + 2:
                # Didn't find a valid candidate -
                # break out of this first item
                break

        if len(cur_walk) == desired_length:
            ret.append(cur_walk)
    return ret


def fuzzy_match_word(word, words, limit):
    """
    Fuzzy find the indexes of word in words, returns a list of indexes which match the
    best return from fuzzy.
    limit controls the number of choices to allow.
    """
    # Try finding exact matches
    exact_matches = set([i for (i, w) in enumerate(words) if w == word])
    if exact_matches:
        logging.debug("Found exact match for {}".format(word))

    # Else, return fuzzy matching
    logging.debug("No exact match for: {}".format(word))
    # Allow some variance which extractOne misses
    # For example: "Armstrong World Industries Inc" in "Armstrong World Industries Inc. agreed in principle to sell its carpet operations to Shaw Industries Inc ."
    best_matches  = [w for (w, s) in process.extract(word, words, processor = semi_process, limit = limit) if (s > 70)]
    logging.debug("Best matches = {}".format(best_matches))
    return list(exact_matches.union([i for (i, w) in enumerate(words) if w in best_matches]))


# Flatten a list of lists
flatten = lambda l: [item for sublist in l for item in sublist]


def semi_process(s, force_ascii=False):
    """
    Variation on Fuzzywuzzy's full_process:
    Process string by
    XX removing all but letters and numbers --> These are kept to keep consecutive spans
    -- trim whitespace
    XX force to lower case --> These are kept since annotators marked verbatim spans, so case is a good signal
    if force_ascii == True, force convert to ascii
    """

    if s is None:
        return ""

    if force_ascii:
        s = asciidammit(s)
    # Remove leading and trailing whitespaces.
    string_out = StringProcessor.strip(s)
    return string_out


if __name__ == '__main__':
    qa_path = 'orig/test.jsonl'
    dist_file = 'q_dist_orig_science_test.json'
    output_file = 'science_test.conll'
    #output_file = 'ls_long_sort_orig_qdist_science_dev.conll'
    write = False
    sort = True
    length = 'long'
    output_eval = True
    QASRL_extractor = QASRL_extractor(qa_path, output_file, dist_file, write, length, sort,
                                      output_eval)
    QASRL_extractor.read()
