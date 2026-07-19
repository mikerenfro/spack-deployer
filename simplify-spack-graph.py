#!/usr/bin/env python

# Simplify the output of "spack graph --dot".
#
# 1. gcc-runtime and glibc nodes are very busy, and rarely useful, so
#    they're removed.
# 2. Node labels are simplified, removing the hash and the compiler.
#
# This greatly improves readability of the remaining graph elements:
# when processed through "dot -Tpdf", the page size for wireshark's
# graph is reduced by 75%, and is readable when zoomed to full width
# on a 27" 2560x1440 screen.
#
# Usage: simplify-spack-graph.py < file.dot | open -f -a Preview

# Other notes on graphs
# edge colors are -- build: dodgerblue, link: crimson, run: goldenrod
# node colors are -- build_dependencies: fillcolor=coral
import re
import sys

label_pattern = r'(label)=\"([^/]*)/(?:[^\"]*)\"'
label_replacement = r'\1="\2"'

lines = sys.stdin.readlines()

# Simplify node labels (remove hash and compiler)
updated_lines = [re.sub(label_pattern, label_replacement, line) for line in lines]

# Find the glibc hash so we can remove all nodes/edges referencing it
glibc_pattern = r'"(\w*)" \[label="glibc@.*'
for l in updated_lines:
    m = re.search(glibc_pattern, l)
    if m:
        glibc_hash = m.groups()[0]
        break
# Find the compiler-wrapper hash so we cna remove all nodes/edges referencing it
compiler_wrapper_pattern = r'"(\w*)" \[label="compiler-wrapper@.*'
compiler_wrapper_hash = None # if we graph only with "run,link" edge types, we never see compiler-wrapper
for l in updated_lines:
    m = re.search(compiler_wrapper_pattern, l)
    if m:
        compiler_wrapper_hash = m.groups()[0]
        break
# Find all gcc-runtime hashes so we can remove all nodes/edges referencing them
gcc_runtime_pattern = r'"(\w*)" \[label="gcc-runtime@.*'
gcc_runtime_hashes = []
for l in updated_lines:
    m = re.search(gcc_runtime_pattern, l)
    if m:
       gcc_runtime_hashes.append(m.groups()[0])

# # print(gcc_runtime_hashes)

# Second, remove any node/edge containing the glibc hash or a gcc-runtime hash
updated_lines2 = []
for l in updated_lines:
    hash_absent = True
    if (glibc_hash not in l) and (str(compiler_wrapper_hash) not in l):
        for hash in gcc_runtime_hashes:
            if hash in l:
                hash_absent = False
                break
        if hash_absent:
            updated_lines2.append(l)
updated_lines = updated_lines2

# Third, remove any unconnected nodes
edge_pattern = r'(".[^"]*") -> (".[^"]*")'
node_pattern = r'(".[^"]*") \[label=".[^"]*"\]'

connected_nodes = []
for l in updated_lines:
    m = re.search(edge_pattern, l)
    if m:
        connected_nodes += m.groups()
connected_nodes = set(connected_nodes)
updated_lines2 = []
for l in updated_lines:
    m = re.search(node_pattern, l)
    if not m:
        updated_lines2.append(l)
    else:
        for g in m.groups():
            if g in connected_nodes:
                updated_lines2.append(l)
updated_lines = updated_lines2

for l in updated_lines:
    print(l.rstrip())
