SHELL = bash
venv_dir := .venv
python_bin := python3
all:	venv
venv: $python_bin) -m vevn $(venv_dir)
	(source $(venv_dir)/bin/activate && pip install -r requirements.txt -U)

