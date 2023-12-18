import sys

import yaml
import jinja2

if len(sys.argv) < 1:
    raise ValueError("Please provide book name")

book = sys.argv[1]

info_filename = f"info/{book}.yaml"
template_filename = f"{book}/index.html.j2"
result_filename = f"public/{book}/index.html"

if book == "root":
    result_filename = "public/index.html"

with open(info_filename, "r") as f:
    info = yaml.safe_load(f)

templateEnv = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="templates"))
template = templateEnv.get_template(template_filename)

with open(result_filename, "w") as f:
    f.write(template.render(info=info))
