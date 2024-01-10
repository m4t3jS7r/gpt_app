# aplikacija gpt_app
Aplikacija omogoča komunikacijo z modelom GPT podjetja OpenAI. Narejena je v obliki IM, kjer se uporabnikova sporočila pošljejo na API (pošlje se tudi zgodovina pogovora). Aplikacija omogoča tvorbo več pogovorov, kjer ima lahko vsak pogovor svoje ime. Aplikacija deluje na namiznih sistemih (npr. windows, linux) in mobilnih napravah (npr. android).

# demo
Fotografije aplikacije se nahajajo v demo mapi.

# dokumentacija
## (obrrazložitev kode)
https://matej.gitbook.io/gpt-app/

# navodila 
## (namestitev in zagon aplikacije)
1. namesti python3
2. v ukazni lupini ustvari navidezno okolje:
    - `cd gpt_app`
    - `python3 -m venv .venv`
    - `.venv\Scripts\activate.bat` (*windows*) 
    - `source .venv\Scripts\activate` (*linux*)
3. namesti pakete potrebne za delovanje aplikacije
    - `python3 -m pip install -r req.txt`
4. zaženi aplikacijo
    - `python3 main.py`