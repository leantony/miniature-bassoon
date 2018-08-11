#! /usr/bin/env python3

import json
import operator
from prettytable import PrettyTable


def read_dataset(filename):
    print("reading file {0}".format(filename))
    with open(filename, 'r') as f:
        content = f.read()
        inner = json.loads(content)
    return inner


def construct_baseline_report(results):
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
    return html


def write_baseline_report(template_file, file_to_write, data_to_write, **kwargs):
    with open(template_file, 'r') as f:
        contents = f.read()
        while '{doc_title}' in contents:
            contents = contents.replace(
                '{doc_title}', 'GIS source tree analysis')
        while '{scanned_path}' in contents:
            contents = contents.replace('{scanned_path}', kwargs['path'])
        while '{file_count}' in contents:
            contents = contents.replace(
                '{file_count}', str(kwargs['count']))
        while '{table_contents}' in contents:
            contents = contents.replace('{table_contents}', data_to_write)

        with open(file_to_write, "w") as f:
            f.write(contents)


dataset_file = "output.json"
template_file = "table_template.html"
out_file = "table.html"

data = read_dataset(dataset_file)
html_output = construct_baseline_report(data['results'])

args = {'path': data['rootPath'], 'count': data['resultCount']}
print(args)
write_baseline_report(template_file, out_file, html_output, **args)
