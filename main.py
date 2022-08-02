import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter

# read source notebook
print("[INFO] open notebook")
with open('test.ipynb') as f:
  nb = nbformat.read(f, as_version=4)

print("[INFO] execute notebook")
# execute notebook
ep = ExecutePreprocessor(timeout=-1, kernel_name='python3')
ep.preprocess(nb) #currently results in a weird error

print("[INFO] export notebook")
# export to html
html_exporter = HTMLExporter()
html_exporter.exclude_input = True
html_data, resources = html_exporter.from_notebook_node(nb)

print("[INFO] write output")
# write to output file
with open("notebook.html", "w", encoding='utf') as f:
  f.write(html_data)

print("[INFO] done")
