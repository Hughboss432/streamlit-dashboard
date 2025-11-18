VENV=.venv
PYTHON=$(VENV)/bin/python3
PIP=$(VENV)/bin/pip
STREAMLIT=$(VENV)/bin/streamlit

$(VENV)/bin/activate: 
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

install: $(VENV)/bin/activate

run: install
	$(STREAMLIT) run main.py