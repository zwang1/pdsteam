import json

with open("yelp.ipynb") as f:
	contents = json.load(f)
	wordcount = 0
	codecount = 0
	for cell in contents["cells"]:
		if cell["cell_type"] == "markdown":
			for line in cell["source"]:
				wordcount += len(line.split())
		elif cell["cell_type"] == "code":
			codecount += len(cell["source"])

print "word count", wordcount
