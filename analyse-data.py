#! /usr/bin/env python3

import json
import operator
from prettytable import PrettyTable

filename = "output.json"
template_src = "table_template.html"

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

# now the table
i = 0
t = PrettyTable(['JavaFile', 'BackendCalls', 'Size'])
for r in results:
    fname = results[i]['fileNameWithPackageName']
    bs = results[i]['backendCalls']
    size = len(bs)
    procs = '\n'.join(bs.keys())
    i = i + 1
    t.add_row([fname, procs, size])
    # if i > 0:
    #     break

t.sortby = "Size"
t.reversesort = True
t.align["JavaFile"] = "l"
t.align["BackendCalls"] = "l"

html = t.get_html_string()

with open(template_src, 'U') as f:
    contents = f.read()
    while '{doc_title}' in contents:
        contents = contents.replace('{doc_title}', 'GIS source tree analysis')
    while '{scanned_path}' in contents:
        contents = contents.replace('{scanned_path}', inner['rootPath'])
    while '{file_count}' in contents:
        contents = contents.replace('{file_count}', str(inner['resultCount']))
    while '{table_contents}' in contents:
        contents = contents.replace('{table_contents}', html)

with open('table.html', "w") as f:
    f.write(contents)
