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
├── data/                  - Dane używane w projekcie
│   ├── external/          - Zewnętrzne źródła danych (np. pobrane z internetu)
│   ├── interim/           - Dane pośrednie, przetworzone częściowo
│   ├── merged_en_de_es.csv - Przykładowy złączony zbiór danych
│   ├── processed/- Dane w pełni przetworzone i gotowe do modelowania
│   └── raw/- Surowe dane wejściowe
│
├── design_proposal.md	- Dokumentacja projektowa / propozycja architektury
│
├── detector/			- Aplikacja Streamlit i backend do detekcji halucynacji
│   ├── app.py		- Interfejs użytkownika (Streamlit)
│   └── backend.py		- Logika detektorów halucynacji i funkcje pomocnicze
│
├── docs/			- Dokumentacja, diagramy, raporty techniczne
│   ├── articles_details.pdf	- analiza literaturowa
│   ├── Raport.pdf		- cała dokumentacja projektu
├── notebooks/		- Notatniki Jupyter z eksperymentami
├── chain_of_thought.ipynb
├── language.ipynb
├── multiple_choice_baseline_critique_consistency.ipynb
├── truthfulqa_baseline_self_critique_self_consistency_analysis.ipynb
├── truthfulqa_experiment.ipynb
│
├── pyproject.toml        - Plik konfiguracyjny dla środowiska Python / build
├── README.md              - Podstawowa dokumentacja i instrukcje uruchomienia
├── reports/               - Raporty i wyniki eksperymentów
│   └── truthfulqa/        - Raporty z eksperymentów TruthfulQA
├── temp.pdf               - Tymczasowy plik PDF do testów RAG / detekcji
└── uv.lock                - Plik blokady środowiska (np. pipenv/poetry)

```

--------

