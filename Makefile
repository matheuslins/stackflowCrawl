
clean: clean-build clean-others clean-pyc clean-test

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr .eggs/
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -f {} +

clean-others:
	@find . -name 'Thumbs.db' -exec rm -f {} \;

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	@rm -fr .tox/
	@rm -f .coverage
	@rm -fr htmlcov/

test:
	@py.test -s tests

coverage:
	@py.test -s tests --cov

coverage.html:
	@py.test -s tests --cov --cov-report=html

pep8:
	@pep8 --filename="*.py" --ignore=W --first --show-source --statistics --count

spider:
	@echo "Criando spider:" $(NAME) "....."
	@echo "Criando diretorio principal"
	@mkdir ./crawlpy/crawlpy/spiders/$(NAME)
	@cd ./crawlpy/crawlpy/spiders/$(NAME) &&\
	mkdir ./constants &&\
	mkdir ./steps &&\
	echo "# spider-arguments.yml\n---" > spider-arguments.yml &&\
	echo "# coverage.py\n---\n" > coverage.py &&\
	echo "# -*- coding: utf-8 -*-\n" > __init__.py &&\
	echo "# -*- coding: utf-8 -*-\n" > spiders.py &&\
	echo "\"\"\"\n\nSpider:"$(NAME)"\n\n\"\"\"" >> spiders.py &&\
	echo "# -*- coding: utf-8 -*-\n" > ./utils.py &&\
	echo "Criando a estrutura de constantes......" &&\
	echo "# -*- coding: utf-8 -*-\n" > ./constants/__init__.py &&\
	echo "# -*- coding: utf-8 -*-\n" > ./constants/consulta.py &&\
	echo "# -*- coding: utf-8 -*-\n" > ./constants/extracao.py &&\
	echo "Criando a estrutura de steps......" &&\
	echo "# -*- coding: utf-8 -*-\n" > ./steps/__init__.py &&\
	echo "# -*- coding: utf-8 -*-\n" > ./steps/consulta.py &&\
	echo "# -*- coding: utf-8 -*-\n" > ./steps/extracao.py
	@echo "Spider criada!"

deps:
	pip install -r requirements.txt

free:
	pip freeze > requirements.txt