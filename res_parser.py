
from resume import res_class

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--filepath',help='This is the path to resume file',required=True)
args = parser.parse_args()

if args.filepath:
    res=res_class(args.filepath)
    res.process()
    res.show_details()

else:
    print("Please enter the correct file path :")    