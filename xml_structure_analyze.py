import os
from tqdm import tqdm
import xml.etree.ElementTree as ET

PATH = './path/to/analyze'



def tree_traversal(ptr_base, ptr_node):
	ptr_base['attribs'] = list(set(ptr_base['attribs'] + list(ptr_node.attrib.keys())))
	child_tags = [c.tag for c in ptr_node]
	ptr_base['child_tags'] = list(set(ptr_base['child_tags'] + child_tags))
	for tag in ptr_base['child_tags']:
		if tag not in ptr_base['children']:
			ptr_base['children'][tag] = {'attribs':[], 'child_tags':[], 'children': {}}
	for chld in ptr_node:
		tree_traversal(ptr_base['children'][chld.tag], chld)

def tree_structure(base, path):
	with open(path, 'r', encoding='utf8') as f:
		root = ET.fromstring(f'<tmp>{f.read().split('\n',1)[1]}</tmp>')
	base['attribs'] = []
	base['child_tags'] = []
	base['children'] = {}
	tree_traversal(base, root)

def tree_out(tab, base_node):
	for ct in base_node['child_tags']:
		print(f'{"\t"*tab}{ct}')
		for attr in base_node['children'][ct]['attribs']:
			print(f'+{attr}')
		print()
		tree_out(tab+1, base_node['children'][ct])




target_files = [f'{PATH}/{x}' for x in os.listdir(PATH) if x.endswith('.xml')]
# target_files = target_files[:2]
res = {}
for t in tqdm(target_files):
	tree_structure(res, t)

tree_out(0, res)
