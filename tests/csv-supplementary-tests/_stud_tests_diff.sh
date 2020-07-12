#!/usr/bin/env bash

# Name:	Lukáš Drahník
# Project: CSV: CSV2XML
# Date:	5.7.2020
# Email: <xdrahn00@stud.fit.vutbr.cz>, <ldrahnik@gmail.com>

# jexamxml.jar
JEXAMXML_JAR_FILE=$1
# jexamxml tmp file
JEXAMXML_TMP_FILE=$2
# options
JEXAMXML_OPTIONS_FILE=$3

# Složky referenčního výstupu a výstupu k porovnání.
OUT_DIR=$4
REF_OUT_DIR=$5

# Projdeme všechny testy.
for TEST_FILE_NAME in $(find $REF_OUT_DIR -type f -name "*.xml" -printf "%f\n" | sort -n); do

    TEST_NAME=${TEST_FILE_NAME%.xml}

    # Zkontrolujeme návratovou hodnotu.
    if diff "$OUT_DIR/$TEST_NAME.!!!" "$REF_OUT_DIR/$TEST_NAME.!!!" > /dev/null; then

        # Pokud návratová hodnota je "0", zkontrolujeme i výstup.
        if [[ $(head -n 1 "$REF_OUT_DIR/$TEST_NAME.!!!") == "0" ]]; then

            # Porovnání výstupu s referenčním provedeme pomocí knihovny JEXAMXML.
            eval $(java -jar $JEXAMXML_JAR_FILE "$OUT_DIR/$TEST_NAME.xml" "$REF_OUT_DIR/$TEST_NAME.xml" $JEXAMXML_TMP_FILE $JEXAMXML_OPTIONS_FILE > /dev/null);
            if [ $? -eq 0 ]; then
                echo "*******TEST $TEST_NAME PASSED";
            # Podrobnější výpis co je rozdílné v případě neshody je uložen do souboru $JEXAMXML_TMP_FILE, který se zobrazí.
            else
                cat $JEXAMXML_TMP_FILE
                echo "TEST $TEST_NAME FAILED";
            fi
        # Pokud návratová hodnota není "0", program byl ukončen předčasně a výstup nebyl generován. Test proběhl úspěšně.
        else
            echo "*******TEST $TEST_NAME PASSED";
        fi
    else
        echo "TEST $TEST_NAME FAILED";
    fi
done
