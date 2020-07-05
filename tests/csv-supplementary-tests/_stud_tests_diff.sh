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
for i in {01..18}; do

    # Zkontrolujeme návratovou hodnotu.
    if diff "$OUT_DIR/test$i.!!!" "$REF_OUT_DIR/test$i.!!!" > /dev/null; then

        # Pokud návratová hodnota je "0", zkontrolujeme i výstup.
        if [[ $(head -n 1 "$REF_OUT_DIR/test$i.!!!") == "0" ]]; then

            # Porovnání výstupu s referenčním provedeme pomocí knihovny JEXAMXML.
            eval $(java -jar $JEXAMXML_JAR_FILE "$OUT_DIR/test$i.xml" "$REF_OUT_DIR/test$i.xml" $JEXAMXML_TMP_FILE $JEXAMXML_OPTIONS_FILE > /dev/null);
            if [ $? -eq 0 ]; then
                echo "*******TEST$i PASSED";
            # Podrobnější výpis co je rozdílné v případě neshody je uložen do souboru $JEXAMXML_TMP_FILE, který se zobrazí.
            else
                cat $JEXAMXML_TMP_FILE
                echo "TEST$i FAILED";
            fi
        # Pokud návratová hodnota není "0", program byl ukončen předčasně a výstup nebyl generován. Test proběhl úspěšně.
        else
            echo "*******TEST$i PASSED";
        fi
    else
        echo "TEST$i FAILED";
    fi
done
