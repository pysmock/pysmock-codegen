import pysmock.logger as logger
log = logger.set_app_level_logger()
import typer
from pysmock.utils.ModelParser import ModelParser  
from typing import Optional, Dict, List
from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader
app=typer.Typer()
import pathlib


path = pathlib.Path(__file__).parent.resolve()    

@app.command()
def main(input_file_name: typer.FileText = typer.Option(...,"--input-file","--input","-i"),
        output: Optional[Path]=typer.Option("../dist", exists=False, writable=True)
        ):
  """
  Arguments: 
  :param --input-file, --input, -i -> input yaml file
  :param --output -> output directory, if exists the contents will be cleared
  """
  if output.exists() and not output.is_dir():
    typer.echo("Output not a directory!")
    exit(1)
  # log.debug(output.absolute())
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
  env = Environment(loader = FileSystemLoader(str(path.absolute())+'/templates'),   trim_blocks=True, lstrip_blocks=True)
  template = env.get_template('flask_app.py')
  f = open(str(output.absolute())+"/app.py", 'w')
  f.write(template.render(model=model))
  f.close()
  log.info('Code Creation completed!')
  pass

if __name__=='__main__':
  typer.run(main)


