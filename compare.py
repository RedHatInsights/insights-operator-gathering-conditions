# Deep-compare two JSON files, ignoring the order of array items.
#
# Output "{}" means the files contain identical data.
#
# To compare two "build" folders:
# BUILD1=build ; BUILD2=build-original; find $BUILD1 -type f | while read FILE1; do echo $FILE1 ; FILE2=`echo $FILE1 |sed "s/$BUILD1/$BUILD2/"` ; python compare.py $FILE1 $FILE2; done

import json
import sys

from deepdiff import DeepDiff


def load_json(path):
    with open(path) as fd:
        return json.load(fd)


a = load_json(sys.argv[1])
b = load_json(sys.argv[2])
ddiff = DeepDiff(a, b, ignore_order=True)

print(ddiff)
