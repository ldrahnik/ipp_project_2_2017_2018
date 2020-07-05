# Name:	Lukáš Drahník
# Project: CLS: C++ Classes
# Date:	5.7.2020
# Email: <xdrahn00@stud.fit.vutbr.cz>, <ldrahnik@gmail.com>

PWD											= $(shell pwd)

############################################ TESTS

JEXAMXML									= $(PWD)/jexamxml.jar
JEXAMXML_OPTIONS_FILE						= $(PWD)/csv-supplementary-tests/csv_options
JEXAMXML_TMP_FILE							= $(PWD)/csv-supplementary-tests/jexamxml_tmp

SUPPLEMENTARY_TESTS_DIRECTORY				= ./tests/csv-supplementary-tests
SUPPLEMENTARY_TESTS_SCRIPT              	= _stud_tests.sh # <where is located cls.php dir> <output dir>
SUPPLEMENTARY_TESTS_SCRIPT_OUTPUT			= $(PWD)/tests/csv-supplementary-tests/out
SUPPLEMENTARY_TESTS_SCRIPT_REF_OUTPUT		= $(PWD)/tests/csv-supplementary-tests/ref-out
SUPPLEMENTARY_TESTS_DIFF_SCRIPT				= _stud_tests_diff.sh # <jexamxml jar file> <jexamxml options file> <output dir> <ref-out dir>

test:
	# pustí projekt s dodanými testy a výstupy uloží do složky
	cd $(SUPPLEMENTARY_TESTS_DIRECTORY) && bash $(SUPPLEMENTARY_TESTS_SCRIPT) $(PWD) $(SUPPLEMENTARY_TESTS_SCRIPT_OUTPUT)
	
	# provede porovnání výstupů
	cd $(SUPPLEMENTARY_TESTS_DIRECTORY) && bash $(SUPPLEMENTARY_TESTS_DIFF_SCRIPT) $(JEXAMXML) $(JEXAMXML_TMP_FILE) $(JEXAMXML_OPTIONS_FILE) $(SUPPLEMENTARY_TESTS_SCRIPT_OUTPUT) $(SUPPLEMENTARY_TESTS_SCRIPT_REF_OUTPUT)
	
	# úklid
	rm -rf $(JEXAMXML_TMP_FILE)
	rm -rf $(SUPPLEMENTARY_TESTS_SCRIPT_OUTPUT)/*
	
