# Hallarch

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Celem pracy jest analiza mechanizmów prowadzących do halucynacji w modelach językowych, opis rodzajów halucynacji, wpływ poszczególnych czynników na częstość ich występowania oraz metody ich wykrywania.
Efektem końcowym projektu będzie raport badawczy zawierający analizę zjawiska, wyniki eksperymentów, interpretację obserwowanych mechanizmów oraz opracowanie metod pozwalających lepiej rozumieć, wykrywać i przeciwdziałać tym zjawiskom.

Użyte modele działały z Ollama, której obraz można łatwo pobrać i uruchomić w Docker:

```commandline
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

Po uruchomieniu konteneru Olla można wprowadzić komendę, która pobierze porządany model LLM (np. llama3.1:8b):

```
docker exec -it ollama ollama pull llama3.1:8b
```



## Project Organization

```
├── Makefile           <- Makefile with convenience commands
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         hallarch and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
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

