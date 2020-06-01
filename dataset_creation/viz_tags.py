""" Usage:
    viz_tags --in=INPUT_FILE --out=OUTPUT_FILE
"""
from matplotlib.backends.backend_pdf import PdfPages
import os
from docopt import docopt
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if __name__ == "__main__":
    args = docopt(__doc__)
    input_fn = args["--in"]
    output_fn = args["--out"]
    df = pd.read_csv(input_fn, sep = "\t", skip_blank_lines = True, header = None)
    print(df.groupby(7).count())
    ax = df.groupby(7).count()[1].plot.pie(autopct='%1.1f%%')
    ax.set_title('distribution of tag labels')
    pp = PdfPages(output_fn)
    fig = ax.get_figure()
    pp.savefig(fig)
    fig.clear()
    pp.close()




