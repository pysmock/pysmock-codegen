__version__ = "0.1.0dev05"
__author__ = 'Harsha Sridhar'
__author_email__='contact.pysmock@gmail.com'
__description__='A tool to generate a mock server from yaml file using python'
REQUEST_TYPE=['get','post','put','delete','head','options']
from pysmock.models import ( APIRequest, Contact, Info, License, MockSetup, Request, Response )
from pysmock.utils import ( GenericFieldParser, ModelParser )
import pkg_resources
import yaml
pkg_resources.declare_namespace(__name__)

import typer
# from utils.ModelParser import ModelParser  
from typing import Optional, Dict, List
from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader
app=typer.Typer()
    

@app.command()
def main(input_file_name: typer.FileText = typer.Option(...,"--input-file","--input","-i"),
        output: Optional[Path]=typer.Option("../dist", exists=False, writable=True),
        ):
  if output.exists() and not output.is_dir():
    typer.echo("Output not a directory!")
    exit(1)
  print(output.absolute())
  generate_code(input_file_name,output)
  pass
import shutil
def generate_code(input_file_name: typer.FileText, output: Path):
  if output.exists():
    shutil.rmtree(str(output.absolute()))
  output.mkdir()

  data = yaml.safe_load(input_file_name)
  model = ModelParser.parseToObject(data)

  f = open(str(output.absolute())+"/Procfile", 'w')
  f.write("web: gunicorn app:app")
  f.close()

  f = open(str(output.absolute())+"/requirements.txt", 'w')
  f.write('''certifi==2020.12.5
click==7.1.2
Flask==1.1.2
Flask-Cors==1.10.3
gunicorn==20.0.4''')
  f.close()
  env = Environment(loader = FileSystemLoader('./templates'),   trim_blocks=True, lstrip_blocks=True)
  template = env.get_template('flask_app.py')
  f = open(str(output.absolute())+"/app.py", 'w')
  f.write(template.render(model=model))
  f.close()
  print('Code Creation completed!')
  pass

if __name__=='__main__':
  typer.run(main)


