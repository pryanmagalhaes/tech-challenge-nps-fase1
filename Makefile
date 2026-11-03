# Reproduz toda a análise do zero: tratamento -> EDA -> apresentação
.PHONY: all install notebooks presentation clean

all: notebooks presentation

install:
	pip install -r requirements.txt

notebooks:
	jupyter nbconvert --to notebook --execute --inplace notebooks/01_qualidade_e_tratamento_dos_dados.ipynb
	jupyter nbconvert --to notebook --execute --inplace notebooks/02_analise_exploratoria_eda.ipynb

presentation:
	python presentation/build_presentation.py

clean:
	rm -f data/processed/*.csv reports/figures/*.png reports/key_metrics.json reports/data_quality_report.csv
