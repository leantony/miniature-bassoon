#! /usr/bin/env python3

import json
import operator
from prettytable import PrettyTable

filename = "output.json"
print("reading file {0}".format(filename))

with open(filename, 'r') as f:
    content = f.read()
    inner = json.loads(content)

# root
results = inner['results']

# metadata
pathUsed = inner['rootPath']
timeTaken = inner['timeTaken']
resultsCount = inner['resultCount']

# r = PrettyTable(['Info', 'message'])
# r.add_row(['Path', pathUsed])
# r.add_row(['ScanTime', timeTaken])
# r.add_row(['ResultsCount', resultsCount])

# now the table
i = 0
t = PrettyTable(['JavaFile', 'BackendCalls'])
for r in results:
    fname = results[i]['fileNameWithPackageName']
    backendCalls = results[i]['numberOfBackendCalls']
    i = i + 1
    t.add_row([fname, backendCalls])

t.sortby = "BackendCalls"
t.reversesort = True
t.align["JavaFile"] = "l"

print(t)
