# Wyjaśnialność halucynacji w modelach językowych

Cezary Dymicki, Krzysztof Żak, Ewelina Trybułowska  
Grupa nr 9

# Wstęp

Duże modele językowe, takie jak GPT, Gemini, Claude czy LLaMA, osiągnęły imponujące wyniki w generowaniu spójnego i logicznego tekstu. Jednak mimo wysokiej jakości językowej, często generują one halucynacje \- treści nieprawdziwe, nie poparte danymi lub całkowicie fikcyjne.

# Opis projektu

Celem pracy jest analiza mechanizmów prowadzących do halucynacji w modelach językowych, opis rodzajów halucynacji, wpływ poszczególnych czynników na częstość ich występowania oraz metody ich wykrywania.

Efektem końcowym projektu będzie raport badawczy zawierający analizę zjawiska, wyniki eksperymentów, interpretację obserwowanych mechanizmów oraz opracowanie metod pozwalających lepiej rozumieć, wykrywać i przeciwdziałać tym zjawiskom.

# Funkcjonalności

* Wykrywanie halucynacji w odpowiedziach zwracanych przez model,  
* Porównywanie ilości halucynacji w zależności od zmian parametrów modelu na różnych etapach uczenia,  
* Opis metod przeciwdziałania halucynacjom oraz ich skuteczności.

# Zakres pracy

* Analiza teoretyczna zjawiska halucynacji  
  * przegląd literatury dotyczącej przyczyn halucynacji w LLM (np. dekodowanie, kontekst, brak wiedzy, bias danych),  
  * zdefiniowanie halucynacji i klasyfikacja typów halucynacji (faktyczne, logiczne, kontekstowe).  
  * klasyfikacja przyczyn: dane treningowe, architektura, kontekst  
* Implementacja środowiska eksperymentalnego  
  * przygotowanie zestawu promptów testowych,  
  * utworzenie mini-indeksu wiedzy (RAG) w oparciu o narzędzia FAISS lub Chroma,  
  * integracja z wybranymi modelami językowymi   
* Przeprowadzenie eksperymentów badawczych  
* Ewaluacja wyników  
  * zastosowanie automatycznych metryk (accuracy, hallucination-rate, precision@evidence, ECE, Brier Score),  
  * przeprowadzenie ręcznej oceny jakości (human evaluation),  
* Opracowanie wniosków i rekomendacji  
  * analiza wyników  
  * identyfikacja czynników najbardziej wpływających na halucynacje,  
  * ocena skuteczności technik ograniczających halucynacje,  
  * sformułowanie zaleceń dla konstrukcji bardziej wiarygodnych systemów generatywnych.  
* Opis metod pozwalających wykrywać halucynacje

# Zakres planowanych eksperymentów

### **1\. Wpływ długości i jakości kontekstu**

**Cel:** sprawdzić, czy przeładowanie promptu zwiększa błędy.

* wymuszenie tej samej odpowiedzi przy krótkim vs długim kontekście (z dodanym „szumem”),  
* analiza przypadków niejednoznacznych promptów.

### **2\. Self-consistency / self-critique**

**Cel:** Ocena, czy mechanizmy samokontroli (self-consistency, self-critique) ograniczają halucynacje.

* Generacja wielu próbek (n ∈ {1, 5, 10}) i agregacja odpowiedzi metodą głosowania (majority voting).  
* Dodatkowo test fazy „self-critique” \- model ocenia własną odpowiedź.

### **3\. Wpływ parametrów dekodowania**

### **Cel:** Zbadanie wpływu parametrów generacji tekstu na częstość halucynacji.

* ### Zmiana parametrów dekodowania:

  * ### Temperatura ∈ {0.0, 0.3, 0.7, 1.0}

  * ### Top-p ∈ {0.7, 0.9, 0.95}

  * ### Beam search vs. greedy decoding

### **4\. Wpływ kontekstu i integracji z RAG**

### **Cel:** Ocena wpływu dołączonych dokumentów (retrieval) na ograniczenie zmyślania informacji.

* ### Stworzenie mini-indeksu (FAISS lub Chroma) z kilku artykułów.

* ### Porównanie generacji:

  * ### bez RAG

  * ### z RAG przy top-k ∈ {3,5,10}

* ### Porównanie metod retrievalu: BM25 vs. dense retrieval.

**5\. Użycie łańcuchu rozumowania (Chain of thought) a częstość halucynacji**  
**Cel:** Czy jawne proszenie o podanie kolejnych etapów “dochodzenia” do odpowiedzi zmniejsza lub zwiększa błędy?

* Podawanie tego samego prompta z dołączoną prośbą o łańcuch rozumowania, np. “uzasadnienie” i analiza częstości występowania halucynacji  
* Wykonanie eksperymentu zarówno dla dwóch typów zadań i porównanie czy któreś jest bardziej podatne na halucynacje  
  * prośba o konkretną wiedzę (np. Ile ludzi mieszka w USA?)  
  * prośba o przekształcenie / analizę tekstu (np. skróć fragment tekstu i wypisz ile razy użyto w nim słów zaczynających się na “K”)  
* Analiza liczby wymaganych kroków w łańcuchu a częstości halucynacji

**6\. Wpływ języka promptu na częstość halucynacji**  
**Cel:** Czy język (polski, angielski…) wpływa na częstość halucynacji?

* Zadawanie identycznego prompta w kilku różnych językach i porównywanie wyników  
* Zadawanie pytań o tematy np. typowo polskie (wiedza o polskiej geografii, kulturze, osobach publicznych) w języku polskim i obcym *// tak samo dla innych języków i tematów*  
* Prośba o odpowiedź na zadane pytanie w języku w którym został napisany prompt oraz w innym języku \- czy wpływa na częstość halucynacji

# Harmonogram pracy

| Termin | Zadanie |
| :---- | :---- |
| 03.11-09.11 | Dokończenie design proposal. Utworzenie repozytorium. Ogłoszenie skończenia design proposal (deadline **5.11.2025**). Utworzenie środowiska projektu, przegląd literatury \- analiza literatury (kilka artykułów naukowych), omówienie i podzielenie zadań. |
| 10.11-16.11 | Dokończenie prototypu. Omówienie postępu projektu. Umówienie się na spotkanie (deadline na spotkania w sprawie prototypu **14.11.2025**) |
| 17.11-23.11 | Implementacja środowiska eksperymentalnego \- Przygotowanie zestawu promptów testowych (różne długości, z szumem, niejednoznaczne pytania). \- Utworzenie mini-indeksu wiedzy z wykorzystaniem FAISS lub Chroma. \- Integracja z wybranymi modelami LLM |
| 24.11-30.11 | Eksperyment 1: wpływ długości i jakości kontekstu \- Przeprowadzenie testów dla krótkich vs długich promptów (również z szumem informacyjnym). \- Analiza jakości odpowiedzi (accuracy, hallucination rate). \- Zbieranie danych do ewaluacji. |
| 01.12-07.12 | Eksperyment 2: Self-consistency i self-critique \- Implementacja mechanizmu generacji wielu próbek (n ∈ {1, 5, 10}) i agregacji wyników (majority voting). \- Test fazy self-critique (model ocenia własną odpowiedź). \- Zbieranie danych i porównanie wyników z baseline. |
| 08.12-14.12 | Eksperyment 3: wpływ parametrów dekodowania \- Przeprowadzenie serii testów dla różnych wartości parametrów: • Temperatura ∈ {0.0, 0.3, 0.7, 1.0} • Top-p ∈ {0.7, 0.9, 0.95} • Beam search vs greedy decoding. \- Analiza wpływu parametrów na jakość i częstość halucynacji. |
| 15.12-21.12 | Eksperyment 4: wpływ integracji z RAG \- Porównanie generacji: • bez RAG • z RAG (top-k ∈ {3, 5, 10}). \- Test różnych metod retrievalu: BM25 vs dense retrieval. \- Ocena wpływu RAG na redukcję halucynacji. |
| 22.12-28.12 | Boże Narodzenie \- w wolnym czasie kończymy to co zostało do zrobienia z poprzednich tygodni  \- Uporządkowanie kodu i wyników eksperymentów. \- Dokończenie zadań z poprzednich tygodni. |
| 29.12-04.01 | Eksperyment 5: wpływ użycia łańcucha rozumowania (Chain of Thought)  Testowanie promptów z i bez prośby o uzasadnienie („pokaż kroki rozumowania”).  Porównanie wyników dla dwóch typów zadań: faktycznych i analitycznych. Analiza liczby kroków vs częstość halucynacji. Eksperyment 6: wpływ języka promptu na częstość halucynacji  –Porównanie wyników dla promptów w różnych językach (PL/EN/... ).  – Testy pytań o wiedzę lokalną (np. polska kultura, geografia) vs globalną.  – Sprawdzenie wpływu języka odpowiedzi na halucynacje.  |
| 05.01-11.01 | Ewaluacja i analiza wyników \-Zastosowanie automatycznych metryk (accuracy, hallucination-rate, precision@evidence, ECE, Brier Score). \- Przeprowadzenie ręcznej oceny jakości (human evaluation) dla wybranych przypadków. \- Opracowanie zbiorczego raportu wyników. Opracowanie wniosków i rekomendacji \+ detekcja halucynacji \- Analiza czynników najbardziej wpływających na halucynacje. \-Ocena skuteczności metod ograniczających halucynacje (self-consistency, RAG, dekodowanie). \- Implementacja i test prostego detektora halucynacji  |
| 12.01-15.01 | Finalizacja i odesłanie projektu (deadline zwolnienia **15.01.2025**) \- Dokończenie dokumentacji i prezentacji wyników. \- Przygotowanie raportu końcowego (wnioski, rekomendacje). \- Ostateczne sprawdzenie kodu i repozytorium. \- Wysłanie projektu (deadline **15.01.2025**). |

# Stack technologiczny

* **Python**  
* **Ruff** \- autoformatter  
* **Uv** \- zarządzanie środowiskiem

*Framework i biblioteki ML:*

* **Hugging Face (transformers, datasets, evaluate)** – framework do obsługi modeli, danych i ewaluacji  
* **Ollama** – alternatywne środowisko uruchamiania modeli LLM  
* **torch** – backend obliczeniowy  
* **UQLM** – detekcja halucynacji przez metryki niepewności  
* **selfcheckgpt** – black-detektor bez zasobów, generacja samples i sprawdzanie spójności

*Retrieval i analiza:*

* **faiss lub chromadb** – mini-indeks wiedzy (RAG)  
* **numpy / scipy** – obliczenia i statystyki  
* **pandas** – analiza wyników  
* **matplotlib / seaborn** – wizualizacje  
* **datasets** \- do ładowania zbiorów testowych (np. TruthfulQA)

*Eksperymenty i zarządzanie:*

* **hydra lub omegaconf** – konfiguracja eksperymentów  
* **wandb lub mlflow** – śledzenie wyników  
* **jupyter / notebook** – prototypowanie i eksploracja wyników

# Bibliografia

* [Why Language Models Hallucinate](https://cdn.openai.com/pdf/d04913be-3f6f-4d2b-b283-ff432ef4aaa5/why-language-models-hallucinate.pdf)  
  // ciekawy artykuł od OpenAI  
* [https://web.archive.org/web/20230326145635/https://dl.acm.org/doi/pdf/10.1145/3571730](https://web.archive.org/web/20230326145635/https://dl.acm.org/doi/pdf/10.1145/3571730)  
  // o halucynacjach w generowaniu języka naturalnego  
* Afolabi, Z., Taleb, A., Kozodoi, N., & Zinovyeva, E. (2025, May 16). *Detect hallucinations for RAG-based systems*. AWS Machine Learning Blog. Retrieved from [https://aws.amazon.com/blogs/machine-learning/detect-hallucinations-for-rag-based-systems/](https://aws.amazon.com/blogs/machine-learning/detect-hallucinations-for-rag-based-systems/)  
  Artkuł opisuje metody wykrywania halucynacji w RAG:  
1. Detektor oparty na LLM \- Używa modelu językowego, który ocenia, czy zdania w odpowiedzi są oparte na dostarczonym kontekście. Przykładowy proces: dane (kontekst \+ pytanie \+ wygenerowana odpowiedź) → zapytanie do LLM, który zwraca score od 0 (całkowicie oparty na kontekście) do 1 (brak oparcia) dla każdego zdania.   
2. Detektor oparty na semantycznej podobieństwie (embeddings) \- Zakłada, że jeśli zdanie jest faktem opartym na kontekście, to jego embedding będzie bardzo podobny do embeddingu kontekstu; jeśli to halucynacja — podobieństwo będzie niskie. Proces: obliczenie embeddingów dla kontekstu i odpowiedzi, następnie np. odjęcie (1 – cosine\_similarity) aby uzyskać „halucynacyjny” score.   
3. BERT stochastic checker \- Idea: wygenerować kilka wariantów odpowiedzi (stochastic samples) z modelu, a następnie porównać je ze sobą — jeśli dane zdanie w odpowiedzi bardzo różni się semantycznie od wariantów, może to wskazywać na halucynację. Autorzy wykorzystują metrykę „BERT Score” (opartą na embeddings) do zmierzenia podobieństwa między zdaniami w różnych generacjach.   
4. Detektor podobieństwa tokenów (token similarity detector) \- Prostsze podejście: sprawdza, ile tokenów (słów) w zdaniu odpowiedzi pokrywa się z tokenami w kontekście, albo używa BLEU/ROUGE. Niskie pokrycie może sugerować halucynację.  
* Alansari, A., & Luqman, H. (2025). *A Comprehensive Survey of Hallucination in Large Language Models: Causes, Detection, and Mitigation*. arXiv. [https://arxiv.org/html/2510.06265v1](https://arxiv.org/html/2510.06265v1)  
  Artykuł prezentuje przegląd badań nad zjawiskiem halucynacji w dużych modelach językowych (LLM) — definiuje, skatalogowuje i analizuje typy takich błędnych generacji („halucynacje”), ich przyczyny w całym cyklu rozwoju modelu, metody wykrywania oraz strategie łagodzenia.   
* Farquhar, S., Kossen, J., Kuhn, L., … & Gal, Y. (2024). Detecting hallucinations in large language models using semantic entropy. *Nature*, 630, 625–630. [https://www.nature.com/articles/s41586-024-07421-0](https://www.nature.com/articles/s41586-024-07421-0)  
  opisuje metodę mierzenia niepewności LLMów, nazwaną semantic entropy, która skupia się na niepewności znaczeniowej odpowiedzi, nie tylko na wariancji słownej. Semantic entropy mierzy niepewność modelu poprzez analizę różnorodności znaczeniowej wielu odpowiedzi na to samo zapytanie. Model generuje kilka odpowiedzi, które następnie są reprezentowane w przestrzeni semantycznej (embeddingi) i grupowane według podobieństwa znaczeniowego. Entropia Shannona obliczona z rozkładu tych grup odzwierciedla poziom niepewności semantycznej — im większa entropia, tym większe ryzyko halucynacji.  
* Deng, W., Li, J., Zhang, H. Y., Li, J., Deng, Z., Cheng, D., & Feng, Z. (2025). Explainable Hallucination Mitigation in Large Language Models: A Survey. Preprints. \- [https://doi.org/10.20944/preprints202505.0456.v1](https://doi.org/10.20944/preprints202505.0456.v1)  
  Artykuł o explainable hallucination mitigation w LLM przedstawia przegląd metod wykrywania i ograniczania halucynacji oraz podkreśla znaczenie wyjaśnialności modeli dla poprawy ich wiarygodności. Autorzy klasyfikują typy halucynacji i omawiają podejścia oparte na analizie rozumowania, wiedzy zewnętrznej i prompt engineeringu.  
* Cleti, Meade & Jano, Pete. (2024). Hallucinations in LLMs: Types, Causes, and Approaches for Enhanced Reliability. \- [https://www.researchgate.net/publication/385085962\_Hallucinations\_in\_LLMs\_Types\_Causes\_and\_Approaches\_for\_Enhanced\_Reliability](https://www.researchgate.net/publication/385085962_Hallucinations_in_LLMs_Types_Causes_and_Approaches_for_Enhanced_Reliability)  
  * Badania przeglądają halucynacje w dużych modelach językowych. Kategoryzują typy: intrinsic, extrinsic, amalgamated, non-factual. Analizują przyczyny: knowledge overshadowing, insufficient representation, failure in extraction, contextual misalignment, semantic entropy. Oceniają wpływy: negatywne w healthcare, research, journalism; pozytywne w creativity jak art. Omawiają detekcję: NER, SBD, probability-based, two-stage framework, hallucination critic, entity-level. Mitigacja: rewriting, multi-scoring, prompt engineering, fine-tuning, DRAD, adversarial testing. Grounding: RAG, fact-checking, knowledge graphs, APIs, self-contradiction detection, vision-language mitigation. Przyszłe: lepsze evaluation, ethics, integration techniques.  
  * Brak przeprowadzonych badań \- to survey, cytuje istniejące badania i benchmarks jak HalluQA dla chińskich LLMs, ale nie testuje własnych modeli ani datasetów.  
* Farquhar, S., Kossen, J., Kuhn, L. et al. Detecting hallucinations in large language models using semantic entropy. Nature 630, 625–630 (2024) \- [https://doi.org/10.1038/s41586-024-07421-0](https://doi.org/10.1038/s41586-024-07421-0)  
  * Badania rozwijają metodę wykrywania halucynacji w dużych modelach językowych za pomocą semantycznej entropii. Skupiają się na confabulations – arbitralnych, błędnych odpowiedziach. Mierzą niepewność na poziomie znaczeń, nie słów. Twoja metoda generuje wiele odpowiedzi, grupuje je semantycznie i oblicza entropię. Działa bez wiedzy domenowej i generalizuje.  
  * Testy na datasetach QA: TriviaQA (wiedza trivia), SQuAD 1.1 (wiedza ogólna), BioASQ (nauki przyrodnicze), NQ-Open (naturalne pytania z Google Search), SVAMP (problemy matematyczne).  
  * Ocena na nowym datasecie FactualBio do generowania biografii (442 znaków średnio), używając GPT-4.  
  * Porównanie z baseline'ami: leksykalna entropia, P(True), token-level entropy, mutual information.  
  * Badanie robustności: różne modele (LLaMA 2 7B/13B/70B, Falcon 7B/40B, Mistral 7B, GPT-4), temperatury (0-1), liczby sampli (10-100), prompty.  
  * Analiza wpływu: wysoka semantyczna entropia wykrywa confabulations, poprawia accuracy o 5-20% przez odrzucanie niepewnych odpowiedzi.  
  * Generalizacja: metoda działa na nieznanych zadaniach, bez task-specific data.  
* The Dawn After the Dark: An Empirical Study on Factuality Hallucination in Large Language Models (Li et al., ACL 2024\) [https://aclanthology.org/2024.acl-long.586.pdf](https://aclanthology.org/2024.acl-long.586.pdf)  
  * Badania skupiają się na halucynacjach faktów w dużych modelach językowych. Analizują trzy aspekty: jak wykrywać halucynacje, skąd się biorą i jak je zmniejszać. Stworzyli benchmark HaluEval 2.0, prostą metodę detekcji i przetestowali różne techniki.  
  * Budowa benchmarku z 8770 pytaniami z domen biomedycyny, finansów, nauki, edukacji i otwartej.  
  * Test detekcji halucynacji: ekstrakcja faktów z odpowiedzi i ich weryfikacja przez GPT-4, porównana z anotacjami ludzkimi (zgodność ponad 92%).  
  * Analiza źródeł halucynacji w etapach pre-trainingu (wpływ liczby tokenów i familiarności wiedzy), SFT (lepsze instrukcje zmniejszają halucynacje), RLHF (efektywne, ale zależy od domeny) i inferencji (diversity decoding zwiększa halucynacje).  
  * Testy mitigacji: RLHF na modelach jak Alpaca i Vicuna, retrieval augmentation (zmniejsza halucynacje o 10-20%), advanced decoding (greedy-nucleus lepiej niż top-p), self-reflexion (działa dla dużych modeli jak Llama 2-Chat 70B), prompt improvement (lepsze opisy zadań pomagają).  
  * Dodatkowe: wpływ kwantyzacji, formatów promptów i liczby dokumentów retrieval na wyniki.  
  * Użyto modeli jak Llama 2-Chat, Vicuna, ChatGPT i Claude.  
* Large Language Models Cannot Self-Correct Reasoning Yet ([https://arxiv.org/abs/2310.01798](https://arxiv.org/abs/2310.01798))   
  * LLMy nie mogą poprawiać swojego rozumowania bez zewnętrznego feedbacku. Po poprawie “intrinsic self-correction” spada performance.  
  * Testy na benchmarkach GSM8K, CommonSenseQA i HotpotQA. Porównano self-correction z oracle labels (poprawa) vs intrinsic self-correction (spadek accuracy).  
  * Użyto modeli GPT-3.5-Turbo, GPT-4, GPT-4-Turbo i Llama-2. Maksymalnie dwie rundy self-correction. Różne temperatury dekodowania.  
  * Ocena różnych promptów do feedbacku. Żaden nie poprawił wyników bez oracle labels.  
  * Porównanie multi-agent debate z self-consistency na GSM8K. Multi-agent nie przewyższa self-consistency przy równych kosztach.  
  * Analiza prompt design w constrained generation. Pokazano, że lepszy initial prompt bije self-correction.