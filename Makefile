SHELL = bash
venv_dir := .venv
python_bin := python3
all:	venv
venv:	
	$(python_bin) -m venv $(venv_dir)
	(source $(venv_dir)/bin/activate && pip install -r requirements.txt -U)

flake8:
	(source $(venv_dir)/bin/activate && flake8 krach-generator)
pylint:
	(source $(venv_dir)/bin/activate && pylint krach-generator)
