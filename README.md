ASSESSMENT 
==========

9/11.5b ([assessment report](https://github.com/ldrahnik/ipp_2_project/issues/16))

CSV: CSV2XML
================

## Příklad spuštění:

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
