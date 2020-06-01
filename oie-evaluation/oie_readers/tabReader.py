""" Usage:
    tabReader --in=INPUT_FILE

Read a tab-formatted file.
Each line consists of:
sent, prob, pred, arg1, arg2, ...

"""

from oie_readers.oieReader import OieReader
from oie_readers.extraction import Extraction
from docopt import docopt
import logging

logging.basicConfig(level = logging.DEBUG)

class TabReader(OieReader):

    def __init__(self):
        self.name = 'TabReader'

    def read(self, fn):
        """
        Read a tabbed format line
        Each line consists of:
        sent, prob, pred, arg1, arg2, ...
        """
        d = {}
        d_list = []
        ex_index = 0
        with open(fn) as fin:
            for line in fin:
                if not line.strip():
                    continue
                data = line.strip().split('\t')
                text, confidence, rel = data[:3]
                rel = rel.rsplit('##') # split from right to avoid # symbol in tokens
                pred_pos = int(rel[1]) if len(rel) == 2 else None
                head_pred_index = pred_pos # TODO: head_pred_index is not necessarily the first predicate index
                # rel is a tuple, where the first element is str and the second element is a list of index
                rel = (rel[0], [pred_pos + i for i, w in enumerate(rel[0].split(' '))]) if len(rel) == 2 else rel[0]
                curExtraction = Extraction(pred=rel,
                                           pred_pos=pred_pos,
                                           head_pred_index=head_pred_index,
                                           sent=text,
                                           confidence=float(confidence),
                                           question_dist="./question_distributions/dist_wh_sbj_obj1.json",
                                           index=ex_index,
                                           raw=line.strip())
                ex_index += 1

                for arg in data[3:]:
                    arg = arg.rsplit('##') # split from right to avoid # symbol in tokens
                    arg_pos = int(arg[1]) if len(arg) == 2 else None
                    # arg is a tuple, where the first element is str and the second element is a list of index
                    arg = (arg[0], [arg_pos + i for i, w in enumerate(arg[0].split(' '))]) if len(arg) == 2 else arg[0]
                    curExtraction.addArg(arg, arg_pos)

                if text not in d:
                    d[text] = []
                    d_list.append([])
                d[text].append(curExtraction)
                d_list[-1].append(curExtraction)
        self.oie = d
        self.oie_list = d_list


if __name__ == "__main__":
    args = docopt(__doc__)
    input_fn = args["--in"]
    tr = TabReader()
    tr.read(input_fn)
