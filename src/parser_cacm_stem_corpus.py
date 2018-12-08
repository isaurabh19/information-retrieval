# -*- coding: utf-8 -*-
import utils
import os

def parse_stem_corpus():
	# reg = re.compile("#\s+[0-9]+(?s)(.*)#")
	with open(os.path.join(utils.BASE_DIR, "data", "cacm_stem.txt"), "r") as fp:
		content = fp.read()
		corpii = content.split("#")
		print(len(corpii))
		for t in corpii[1:]:
			y = t.split()
			# print(t)
			zeroes = 4 - len(y[0])
			doc_id = 'CACM_{}{}.txt'.format('0'*zeroes, y[0])
			filename = os.path.join(utils.BASE_DIR, "data", "stem_corpus", doc_id)
			z = ' '.join(y[1:])
			with open(filename, "w") as fwp:
				fwp.write(z)

parse_stem_corpus()