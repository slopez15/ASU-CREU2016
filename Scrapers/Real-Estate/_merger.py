import os
import glob

interesting_files = glob.glob(os.getcwd() + "/*.csv")

header_saved = False
with open('_all_properties.csv','w') as fout:
    for filename in interesting_files:
        with open(filename) as fin:
            header = next(fin)
            if not header_saved:
                fout.write(header)
                header_saved = True
            for line in fin:
                fout.write(line)
