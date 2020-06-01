import pandas as pd
from nltk.parse import CoreNLPDependencyParser



parser = CoreNLPDependencyParser(url='http://localhost:9001')
fin = 'oie_corpus/science_eval.oie'
fout = 'oie_corpus/science_eval.oie.correct.head'

with open(fin) as fi, open(fout, 'a') as fo:
	for line in fi:
		data = line.strip().split('\t')
		sent = data[0]
		try:
			parse, = parser.raw_parse(sent)
		except:
			continue
		df = pd.DataFrame([x.split('\t') for x in parse.to_conll(3).split('\n')], columns = ['word', 'pos', 'depth'])

		line = line.rstrip()
		line += '\t' + '<SYN_HEAD>'
		args = data[1:]

		word_list = list(df['word'])
		depth_list = list(df['depth'])
		for arg in args:
			arg = arg.split(' ')
			for i, w in enumerate(word_list):
				if word_list[i:i+len(arg)] == arg:
					print(arg)
					candidate_words = word_list[i:i+len(arg)]
					candidate_depths = depth_list[i:i+len(arg)]
					min_depth = min(candidate_depths)
					head_indices = [i for i, w in enumerate(candidate_words) if candidate_depths[i] == min_depth]
                                        print(head_indices)
                                        head_indices_filtered = []
					head_filtered = []
                                        #take the first continous span at the min syntactic depth
					for i,index in enumerate(head_indices):
                                        	if i == 0:
							head_indices_filtered.append(index)
							head_filtered.append(candidate_words[index])
						else:
							if head_indices[i] - 1 == head_indices[i - 1]:
								head_indices_filtered.append(index)
								head_filtered.append(candidate_words[index])
							else:
								break
                                        print(head_indices_filtered)
					print(head_filtered)
					
                                        line += '\t' + ' '.join(head_filtered)
					break
		fo.write(line)
		fo.write('\n')
