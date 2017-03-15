import os
import time
import json
import codecs

json_file = r"C:/tmp/dict_cnt.json"
with open(json_file, "r") as f:
    data = json.load(f)
    print data

data1 = sorted(data.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
print data1

sorted_json_file = r"C:/tmp/sorted_dict_cnt.json"
with codecs.open(sorted_json_file, "w", "utf-8") as report:
    json.dump(data1, report, ensure_ascii=False, sort_keys=False, indent=4, encoding="utf-8")
