ASSESSMENT 
==========

9/11.5b ([assessment report](https://github.com/ldrahnik/ipp_2_project/issues/16))

CSV: CSV2XML
================

## Příklad spuštění:

```
python3.6 csv.py --help
usage: python3.6 csv.py [--help] [--input INPUT] [--output OUTPUT] [-n]
                        [-r ROOT_ELEMENT] [-s SEPARATOR] [-h [SUBST]]
                        [-c [COLUMN_ELEMENT]] [-l [LINE_ELEMENT]] [-i]
                        [--start START] [-e] [--missing-field MISSING_FIELD]
                        [--all-columns] [--padding] [--validate]

Script na konverzi formátu CSV (viz RFC 4180) do XML. Pro správnou funkčnost
je nutná verze Python3.6.

optional arguments:
  --help                nápověda
  --input INPUT         zadaný vstupní CSV soubor v UTF-8
  --output OUTPUT       textový výstupní XML soubor s obsahem převedeným ze
                        vstupního souboru
  -n                    negenerovat XML hlavičku na výstup skriptu (vhodné
                        například v případě kombinování více výsledků)
  -r ROOT_ELEMENT       jméno párového kořenového elementu obalující výsledek
  -s SEPARATOR          nastavení separátoru (jeden znak) buněk (resp.
                        sloupců) na každém řádku vstupního CSV
  -h [SUBST]            první řádek (přesněji první záznam) CSV souboru slouží
                        jako hlavička a od něj jsou odvozena jména elementů
                        XML
  -c [COLUMN_ELEMENT]   určuje prefix jména elementu column-elementX, který
                        bude obalovat nepojmenované sloupce (implicitně col)
  -l [LINE_ELEMENT]     jméno elementu, který obaluje zvlášť každý řádek
                        vstupního CSV (implicitně row)
  -i                    zajistí vložení atributu index s číselnou hodnotou do
                        elementu line-element
  --start START         inicializace inkrementálního čitače pro parametr -i na
                        zadané kladné celé číslo n včetně nuly (implicitně n =
                        1)
  -e, --error-recovery  zotavení z chybného počtu sloupců na neprvním řádku
  --missing-field MISSING_FIELD
                        missing field filler
  --all-columns         parametr je povolen pouze v kombinaci s --error-
                        recovery (resp. -e), sloupce, které jsou v nekorektním
                        CSV navíc, nejsou ignorovány, ale jsou také vloženy do
                        výsledného XML
  --padding             Provide compact output
  --validate            pokročilá validace vstupního CSV souboru vůči
                        striktnímu výkladu RFC 4180
```

## Omezení programu:

## Rozšíření programu:

## Testování programu:

```
make test
# pustí projekt s dodanými testy a výstupy uloží do složky
cd ./tests/csv-supplementary-tests && bash _stud_tests.sh  /home/ldrahnik/projects/ipp_project_2_2016_2017 /home/ldrahnik/projects/ipp_project_2_2016_2017/tests/csv-supplementary-tests/out
# provede porovnání výstupů
cd ./tests/csv-supplementary-tests && bash _stud_tests_diff.sh  /home/ldrahnik/projects/ipp_project_2_2016_2017/jexamxml.jar /home/ldrahnik/projects/ipp_project_2_2016_2017/csv-supplementary-tests/jexamxml_tmp /home/ldrahnik/projects/ipp_project_2_2016_2017/csv-supplementary-tests/csv_options /home/ldrahnik/projects/ipp_project_2_2016_2017/tests/csv-supplementary-tests/out /home/ldrahnik/projects/ipp_project_2_2016_2017/tests/csv-supplementary-tests/ref-out
*******TEST01 PASSED
*******TEST02 PASSED
*******TEST03 PASSED
*******TEST04 PASSED
*******TEST05 PASSED
*******TEST06 PASSED
*******TEST07 PASSED
*******TEST08 PASSED
*******TEST09 PASSED
*******TEST10 PASSED
*******TEST11 PASSED
*******TEST12 PASSED
*******TEST13 PASSED
*******TEST14 PASSED
*******TEST15 PASSED
*******TEST16 PASSED
*******TEST17 PASSED
*******TEST18 PASSED
# úklid
rm -rf /home/ldrahnik/projects/ipp_project_2_2016_2017/csv-supplementary-tests/jexamxml_tmp
rm -rf /home/ldrahnik/projects/ipp_project_2_2016_2017/tests/csv-supplementary-tests/out/*
```

## Odevzdané soubory:

```
make tree
tree -a xdrahn00-CSV
xdrahn00-CSV
├── CSV-doc.pdf
├── csv.py
├── README.md
└── rozsireni

0 directories, 4 files
```
