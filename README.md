# EasyCite

A simple Python script to download bibtex citations and paper PDFs. Bibtex files pulled from [http://dx.doi.org](http://dx.doi.org/) and PDFs downloaded from SciHub using [scidownl](https://pypi.org/project/scidownl/). 

## How to use

First set up where you want your pdf and bib files to be saved. This is done in the `config.py` file. Each bibliogrpahy is stored as a nested dictionary. When the program starts it will ask you which bibliogrpahy you want to use (i.e. where will the files be saved). 

```
directoryDict = {
    'Bibliography1': {
        'bib':'/path/to/directory/where/bib/files/saved/bib',
        'pdf':'/path/to/directory/where/pdf/files/saved/pdf'
        },
    'Bibliography2': {
        'bib':'/path/to/directory/where/bib/files/saved/bib',
        'pdf':'/path/to/directory/where/pdf/files/saved/pdf'
        }
}
```

Next execute the script with `python EasyCite.py`. Then just copy a doi to the clipboard and press enter.

To quit just type `q`.

![](assets/EasyCite.gif)

## Dependencies

- pyperclip
- bibtexparser
- scidownl.scihub
- termcolor

## Statement

Do not do illegal things with this..

## Statement 2

Elsevier makes £2 billion a year restricting access to publicly funded research..