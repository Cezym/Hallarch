# Hallarch

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

## Cel pracy
Celem pracy jest analiza mechanizmów prowadzących do halucynacji w modelach językowych, opis rodzajów halucynacji, wpływ poszczególnych czynników na częstość ich występowania oraz metody ich wykrywania.
Efektem końcowym projektu będzie raport badawczy zawierający analizę zjawiska, wyniki eksperymentów, interpretację obserwowanych mechanizmów oraz opracowanie metod pozwalających lepiej rozumieć, wykrywać i przeciwdziałać tym zjawiskom.

## Pobranie zależności za pomocą uv
1. Należy zainstalować narzędzie do zarządzania wirtualnymi środowiskami UV (podobne do Condy). Polecenia
wykorzystywane do zainstalowania jej można znaleźć na jej oficjalnej stronie (https://docs.astral.sh/uv/).

Dla macOS i linux:
```commandline
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Dla Windows:
```commandline
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
2. Po zainstalowaniu UV, aby pobrać zależności projektu należy wywołać w terminalu poleceniem

```commandline
uv sync
```

## Ollama
Użyte modele działały z Ollama, której obraz można łatwo pobrać i uruchomić w Docker:

```commandline
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

Po uruchomieniu konteneru Ollama można wprowadzić komendę, która pobierze porządany model LLM (np. llama3.1:8b):

```
docker exec -it ollama ollama pull llama3.1:8b
```

Lub od razu wszystkie użyte w projekcie:
- deepseek-v2:16b
- gemma3:12b
- llama3.1:8b
- mistral:7b

```
docker exec -it ollama ollama pull deepseek-v2:16b && docker exec -it ollama ollama pull gemma3:12b && docker exec -it ollama ollama pull llama3.1:8b && docker exec -it ollama ollama pull mistral:7b
```



## Struktura projektu

```
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- The docs folder
│
├── notebooks          <- Jupyter notebooks
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         hallarch and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│
└── hallarch   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes hallarch a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

