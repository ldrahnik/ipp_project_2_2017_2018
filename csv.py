#!/bin/env python3.6
#CSV:xdrahn00

import argparse, sys
import _csv as csv_sys
import re
import copy

class csv2xml:

    # konstruktor
    def __init__(self):

        # parsování argumentů z příkazové řádky
        opts = self.parseCmdArgs()

        # vykonání konverze
        self.runConversionFromCsv2Xml(opts)

        return

    # spočítá řádky, sloupce, zarovnání pro řádky, sloupce
    def getBaseInfoFromCsvFile(self, opts, separator, all_collumns):
        rowCount = opts.start
        columnsCount = 0

        rowPadding = []
        columnsPadding = []

        tmp = copy.copy(opts.input)
        try:
            tmpCsv = csv_sys.reader(tmp,delimiter=opts.separator, quotechar='"')

            for rows in tmpCsv:
                if columnsCount == 0:
                    columnsCount = len(rows)
                for row in rows:
                    rowCount += 1
                    if all_collumns == True:
                        columnsPadding.append(self.nCharPaddingRequired(max(len(row), columnsCount)))
                    else:
                        columnsPadding.append(self.nCharPaddingRequired(columnsCount))

                rowPadding = self.nCharPaddingRequired(rowCount)
        except csv_sys.Error:
            self.error("nevalidní formát vstupního souboru", 4)

        # uklizení
        del tmpCsv
        del tmp

        return rowCount, columnsCount, rowPadding, columnsPadding

    # validuje CSV soubor (některé errory jsou podmíněné zapnutým --validate)
    def validateCsvFile(self, opts):
        tmpInput = copy.copy(opts.input)

        lines = []
        lineColumns = []

        # RFC 4180: field = (escaped / non-escaped)
        isEscapedField = False

        # byl \r použitý (slouží pro kontrolu následujícího \n, konce řádku)
        crUsed = False

        # byl DQUOTE v escape fieldu poslední znak (slouží pro kontrolu následujícího ")
        dQuoteUsed = False

        # aktuální char
        char = None
        asciiValue = None

        # pozice aktuálního charu
        index = 0

        # pozice konce poslední položky
        lastFieldEndIndex = 0

        # input jako jeden dlouhý string (kvůli podpoře multiline, tzn. přistupování k začátku a konci položky na jiném řádku)
        tmpInputLikeString = ''.join(tmpInput)

        # prázdné CSV => 1 buňka (RFC: Within the header and each record, there may be one or more fields, separated by commas.)
        isEmpty = False
        if len(tmpInputLikeString) == 0 and opts.validate == True:
            isEmpty = True
            lineColumns.append("")
            lines.append(lineColumns)
        else:
           while index < len(tmpInputLikeString):
               char = tmpInputLikeString[index]

               # asci hodnota aktuálního znaku
               asciiValue = ord(char)

               if char == '"' and isEscapedField == False:
                   if index != 0 and tmpInputLikeString[index - 1] != opts.separator and opts.validate == True:
                       self.error("Pokud buňka (anglicky field ) obsahuje ouvozovkovaný řetězec, tak nesmí obsahovat žádné znaky mezi separátory a ohraničujícími uvozovkami", 39)
                   isEscapedField = True
               elif char == '"' and (len(tmpInputLikeString) == index + 1 or tmpInputLikeString[index + 1] == opts.separator or tmpInputLikeString[index + 1] == '\r') and isEscapedField == True and dQuoteUsed == False:
                   isEscapedField = False
                   if len(tmpInputLikeString) != index + 1 and tmpInputLikeString[index + 1] != opts.separator and tmpInputLikeString[index + 1] != '\r' and opts.validate == True:
                       self.error("Pokud buňka (anglicky field ) obsahuje ouvozovkovaný řetězec, tak nesmí obsahovat žádné znaky mezi separátory a ohraničujícími uvozovkami", 39)
               elif char == opts.separator and isEscapedField == False:
                   lineColumns.append(tmpInputLikeString[lastFieldEndIndex:index])
                   lastFieldEndIndex = index + 1
               elif char == "\r" and isEscapedField == False:
                   crUsed = True
               elif char == "\n" and isEscapedField == False:
                   if crUsed == False:
                       self.error("řádky se musí oddělovat pomocí CRLF, znak \\r\\n", 4)
                   crUsed = False

                   # přidání sloupce
                   lineColumns.append(tmpInputLikeString[lastFieldEndIndex:index - 1])
                   lastFieldEndIndex = index + 1

                   # vytvoření záznamu řádku s danými sloupci
                   lines.append(lineColumns)
                   lineColumns = []
               else:
                   dQuoteUsed = self.validateFieldBlock(opts, char, asciiValue, isEscapedField, dQuoteUsed)

               index += 1

        # kontrola hraničních dvojitých uvozovek
        if isEscapedField == True:
            self.error('neukončené dvojité uvozovky položky', 4)

        # kontrola dvojitých uvozovek uvnitř
        if dQuoteUsed == True and opts.validate == True:
            self.error('chybně použité dvojité uvozovky uvnitř hraničním dvojitých uvozovek', 39)

        # kontrola konce řádku
        if crUsed == True:
            self.error('nedošlo na znak LF po CR', 4)

        # přidání sloupce
        lineColumns.append(tmpInputLikeString[lastFieldEndIndex+1:index])

        # vytvoření záznamu řádku s danými sloupci
        lines.append(lineColumns)

        # kontrola konce posledního řádku
        if (char == '\r' or char == '\n') and opts.validate == False:
            self.error('poslední řádek nesmí končit oddělovačem řádku', 4)

        # kontrola počtu sloupců
        firstLineColumCount = None
        lineCount = 0;

        for line in lines:
            lineCount += 1
            if firstLineColumCount == None:
                firstLineColumCount = len(line)
            elif len(line) != firstLineColumCount and opts.e == False:
                self.error('počet sloupců: {:d} na řádku: {:d} nesouhlasí s požadovanými: {:d}'.format(len(line), lineCount, firstLineColumCount), 32)

        # -h=subst vyžaduje první řádek pro určení názvů sloupců
        if opts.subst != None:
            if firstLineColumCount == None:
                self.error("první řádek nemá žádné sloupce!", 31)

        # uklizení
        del tmpInput

        return isEmpty

    # RFC4180: field = (escaped / non-escaped)
    def validateFieldBlock(self, opts, char, asciiValue, isEscapedField, dQuoteUsed):
        if isEscapedField == True:
            if char == "\"":
                dQuoteUsed = not dQuoteUsed
            elif dQuoteUsed == True and opts.validate == True:
                self.error('uvozovky v ouvozovkovaném řetězci se píší jako dva znaky uvozovek vedle sebe. Ascii hodnota znaku který byl předán místo druhé uvozovky: {:d}'.format(asciiValue), 4)
            elif self.validateEscapedBlock(asciiValue) == False and opts.validate == True:
                self.error('znak: \'{:s}\' má ASCI hodnotu: \'{:d}\' a není povolen v escaped TEXTDATA neterminálu'.format(char, asciiValue), 39)
        else:
            if self.validateNonEscapedBlock(asciiValue) == False and opts.validate == True:
                self.error('znak: \'{:s}\' má ASCI hodnotu: \'{:d}\' a není povolen v non escaped TEXTDATA neterminálu'.format(char, asciiValue), 39)

        return dQuoteUsed

    # RFC4180: TEXTDATA =  %x20-21 / %x23-2B / %x2D-7E
    #
    # Školní upřesňující zadání:
    # Pro účely této úlohy je ještě nutné rozšířit definici neterminálu TEXTDATA z RFC 4180, aby
    # akceptovala i UTF-8 znaky s kódem větším jak 127.
    def validateTextDataBlock(self, asciiValue):
        if not (asciiValue == 20) and not (asciiValue == 21) and not (asciiValue > 22 and asciiValue < 44) and not (asciiValue > 44 and asciiValue < 177) and not (asciiValue > 127):
            return False
        return True

    # RFC4180: escaped = DQUOTE *(TEXTDATA / COMMA / CR / LF / 2DQUOTE) DQUOTE
    def validateEscapedBlock(self, asciiValue):
        if not (self.validateTextDataBlock(asciiValue)) and not (asciiValue == 44) and not asciiValue == 13 and not asciiValue == 10 and not asciiValue == 34:
           return False
        return True

    # RFC4180: non-escaped = *TEXTDATA
    def validateNonEscapedBlock(self, asciiValue):
        if self.validateTextDataBlock(asciiValue) == False:
           return False
        return

    # nahradí všechny nepovolené znaky řetězcem
    def replaceDoNotAllowedChars(self, colNames, subst):
        colNames = [s.replace(' ', subst) for s in colNames]
        colNames = [s.replace(',', subst) for s in colNames]
        colNames = [s.replace('\n', subst) for s in colNames]
        colNames = [s.replace('\r', subst) for s in colNames]
        colNames = [s.replace('\t', subst) for s in colNames]
        return colNames

    # provede konverzi z CSV do XML
    def runConversionFromCsv2Xml(self, opts):
        # výstupní xml
        outputXml = ''

        # přednačte soubor kvůli obecným informacím
        linesCount, columnsCount, rowPadding, columnsPadding = self.getBaseInfoFromCsvFile(opts, opts.separator, opts.all_collumns)

        # zvaliduje CSV soubor
        isEmpty = self.validateCsvFile(opts)

        # prázdné CSV => 1 buňka
        if isEmpty == True:
            outputXml += '<?xml version="1.0" encoding="UTF-8"?>\n'

            # obalující element řádku (začátek)
            outputXml += self.getRowStartElement(0, opts.line_element, opts.i, opts.start, rowPadding, opts.padding)

            # přidáme sloupec
            outputXml += self.getColumnElement(opts, 0, 'col1', "")

            # obalující element řádku (konec)
            outputXml += self.getRowEndElement(0, opts.line_element)

            # zápis výsledného XML
            print(outputXml, end='', file=opts.output)

            return 0

        # načteme soubor pomocí knihovny csv
        inputCsv = csv_sys.reader(opts.input, delimiter=opts.separator, quotechar='"')

        # ic = počítadlo odsazení
        ic = 0

        # xml hlavička
        if not opts.n:
            outputXml += '<?xml version="1.0" encoding="UTF-8"?>\n'

        # obalující root element (začátek)
        if opts.root_element != None:
            outputXml += self.getRootStartElement(opts.root_element)
            ic += 1

        # -h=subst
        if opts.subst != None:
            # první řádek je ignorovaný
            linesCount -= 1

            colNames = next(inputCsv)

            # nahradí nepovolené znaky
            colNames = self.replaceDoNotAllowedChars(colNames, opts.subst)
        else:
            colNames = []
            for x in range(1, columnsCount + 1):
                colNames.append('{:s}{:d}'.format(opts.column_element, x))

        # kontrola názvu sloupců
        for name in colNames:
            if self.isValidXmlTagValue(name) != None:
                self.error("nevalidní název sloupce: <"+name, 31)

        # počítadlo řádků
        rc = 0

        for row in inputCsv:

            # obalující element řádku (začátek)
            outputXml += self.getRowStartElement(ic, opts.line_element, opts.i, opts.start, rowPadding, opts.padding)

            # počítadlo sloupců
            cc = 1

            # vložíme sloupce
            for col in row:

                if cc <= columnsCount or opts.all_collumns:
                    if cc <= columnsCount:
                        if opts.padding == False:
                            col_name = colNames[cc-1]
                        else:
                            col_name = self.getColumnName(opts.column_element, cc, columnsPadding[rc], opts.padding)
                    elif opts.all_collumns == True:
                        col_name = self.getColumnName(opts.column_element, cc, columnsPadding[rc], opts.padding)

                    # přidáme sloupec
                    outputXml += self.getColumnElement(opts, ic, col_name, col)
                cc += 1

            # vloží sloupce které jsou navíc (s hodnotou opts.missing_field)
            if opts.all_collumns == True:
                for x in range(cc, columnsCount+1):
                    if cc <= columnsCount:
                        insert_column = colNames[x-1]
                    else:
                        insert_column = self.getColumnName(opts.column_element, x, columnsPadding[rc], opts.padding)

                    # přidáme sloupec
                    outputXml += self.getColumnElement(opts, ic, insert_column, opts.missing_field)

            # obalující element řádku (konec)
            outputXml += self.getRowEndElement(ic, opts.line_element)

            # inkrement čítače indexu
            if opts.i == True:
                opts.start += 1

            # inkrement počítadla řádků
            rc += 1

        # obalující root element (konec)
        if opts.root_element != None:
            outputXml += self.getRootEndElement(opts.root_element)

        # zápis výsledného XML
        print(outputXml, end='', file=opts.output)

        # uklizení
        del inputCsv

        return 0

    # počáteční element, obsah a koncový element sloupce
    def getColumnElement(self, opts, ic, name, value):
        outputXml = ''
        outputXml += self.getColumnStartElement(ic+1, name)
        outputXml += self.getColumnValue(ic+2, value)
        outputXml += self.getColumnEndElement(ic+1, name)
        return outputXml

    # validování argumentů
    def validateCmdArgs(self, args):
        # --help
        if args.help:
            if len(sys.argv) != 2:
                self.error("parameter help nelze kombinovat s žádným dalším parametrem", 1)
            return

        # --input=filename
        if args.input == None:
            args.input = sys.stdin
        else:
            try:
                args.input = open(args.input, mode='r', newline='', encoding='utf-8')
            except IOError:
                self.error("vstupní soubor se nepodařilo otevřít", 2)
        args.input = args.input.readlines()

        # --output=filename
        if args.output == None:
            args.output = sys.stdout
        else:
            try:
                args.output = open(args.output, mode='w', newline='', encoding='utf-8')
            except IOError:
                self.error("výstupní soubor se nepodařilo otevřít pro zápis", 3)

        # -r=root-element
        if args.root_element != None:
            if not self.isValidXmlTagName(args.root_element):
                self.error("nevalidní xml root element předaný parametrem -r: <"+args.root_element, 30)

        # -s=separator
        if args.separator != None and (args.separator.__len__() != 1 and args.separator != 'TAB'):
            self.error("separátor nastavovaný skrze parameter -s musí být pouze jeden znak", 1)

        # -c=column-element
        if args.column_element != None:
            if not self.isValidXmlTagName(args.column_element):
                self.error("nevalidní xml column element předaný parametrem -c: <"+args.column_element, 30)

        # -l=line-element
        if args.line_element != None:
            if not self.isValidXmlTagName(args.line_element):
                self.error("nevalidní xml line element předaný parametrem -l: <"+args.line_element, 30)

        # -i
        if args.i and args.line_element == None:
            self.error("-i parameter se musí kombinovat s parametrem -l", 1)

        # --start=n
        if args.start != None:
            if args.start < 0:
                self.error("hodnota parametru --start=n musí být >= 0", 1)
            if not args.i or args.line_element == None:
                self.error("parameter --start se musí kombinovat s parametrem -i a -l", 1)

        # -e, --error-recovery
        argcopy = []
        for s in sys.argv:
            argcopy.append(re.sub('--error-recovery', '-e', re.sub('\=.*$','', s)))
        if len(argcopy) != len(set(argcopy)):
            self.error("vstupní parametry se nesmí opakovat", 1)

        # --validate
        if args.validate == True:
            if len(sys.argv) > 3 or ((len(sys.argv) < 4) and (args.input == None or args.output == None)):
                self.error("vstupní parametr --validate nelze kombinovat s žádným dalším parametrem kromě --input a --output", 1)

        # --missing-field=val
        if args.missing_field != None:
            if not args.e:
                self.error("parameter --missing-field je povolen pouze v kombinaci s --error-recovery, -e", 1);

        # --all-columns
        if args.all_collumns:
            if not args.e:
                self.error("parameter --all-columns je povolen pouze v kombinaci s --error-recovery, -e", 1);

        return

    # donastavování argumentů
    def setUpCmdArgs(self, args):

        # -s=separator
        if args.separator == None:
            args.separator = ','
        elif args.separator == 'TAB':
            args.separator='\t'

        # -c=column-element
        if args.column_element == None:
            args.column_element = 'col'

        # -l=line-element
        if args.line_element == None:
            args.line_element = 'row'

        # --start=n
        if args.start == None:
            args.start = 1

        # -e, --error-recovery
        if args.e:
            if args.missing_field == None:
                args.missing_field = ''

        return args

    # parsování argumentů z příkazové řádky
    def parseCmdArgs(self):
        # vytváří argumentační parser
        args = argparse.ArgumentParser(prog='python3.6 csv.py', add_help=False, description='Script na konverzi formátu CSV (viz RFC 4180) do XML. Pro správnou funkčnost je nutná verze Python3.6.')

        # nápověda
        args.add_argument('--help', dest='help', action='store_true', help='nápověda')

        # standartní argumenty
        args.add_argument('--input', dest='input', help='zadaný vstupní CSV soubor v UTF-8')
        args.add_argument('--output', dest='output', help='textový výstupní XML soubor s obsahem převedeným ze vstupního souboru')
        args.add_argument('-n', dest='n', action='store_true', help='negenerovat XML hlavičku na výstup skriptu (vhodné například v případě kombinování více výsledků)')
        args.add_argument('-r', dest='root_element', help='jméno párového kořenového elementu obalující výsledek')
        args.add_argument('-s', dest='separator', action='store', help='nastavení separátoru (jeden znak) buněk (resp. sloupců) na každém řádku vstupního CSV')
        args.add_argument('-h', dest='subst', action='store', nargs='?', const='-', help='první řádek (přesněji první záznam) CSV souboru slouží jako hlavička a od něj jsou odvozena jména elementů XML')
        args.add_argument('-c', dest='column_element', action='store', help='určuje prefix jména elementu column-elementX')
        args.add_argument('-l', dest='line_element', action='store', nargs='?', const='row', help='jméno elementu, který obaluje zvlášť každý řádek vstupního CSV')
        args.add_argument('-i', dest='i', action='store_true', help='zajistí vložení atributu index s číselnou hodnotou do elementu line-element')
        args.add_argument('--start', dest='start', action='store', type=int, help='inicializace inkrementálního čitače pro parametr -i na zadané kladné celé číslo n včetně nuly (implicitně n = 1)')
        args.add_argument('-e', '--error-recovery', dest='e', action='store_true', help='zotavení z chybného počtu sloupců na neprvním řádku')
        args.add_argument('--missing-field', dest='missing_field', action='store', help='missing field filler')
        args.add_argument('--all-columns', dest='all_collumns', action='store_true', help='parametr je povolen pouze v kombinaci s --error-recovery (resp. -e), sloupce, které jsou v nekorektním CSV navíc, nejsou ignorovány, ale jsou také vloženy do výsledného XML')

        # rozšíření PAD
        args.add_argument('--padding', dest='padding', action='store_true', help='Provide compact output')

        # rozšíření VLC
        args.add_argument('--validate', dest='validate', action='store_true', help='pokročilá validace vstupního CSV souboru vůči striktnímu výkladu RFC 4180');

        # parsování argumentů
        result = args.parse_args()

        # validování argumentů
        self.validateCmdArgs(result)

        # --help
        if result.help == True:
            args.print_help()
            sys.exit(0)

        # donastavování argumentů
        result = self.setUpCmdArgs(result)

        return result

    # vrátí počáteční element řádku
    def getRowStartElement(self, ic, name, i, n, padLines, padding):
        index = '';
        if i == True:
            index = ' index="{:s}"'.format(self.padNumber(n, padLines, padding))

        return '{:s}<{:s}{:s}>\n'.format(
            self.indent(ic),
            name,
            index
        )

    # vrátí koncový element řádku
    def getRowEndElement(self, ic, name):
        return '{:s}</{:s}>\n'.format(self.indent(ic), name)

    # vrátí počáteční root element
    def getRootStartElement(self, name):
        return '<{:s}>\n'.format(name)

    # vrátí koncový root element
    def getRootEndElement(self, name):
        return '</{:s}>\n'.format(name)

    # vrátí počáteční element sloupce
    def getColumnStartElement(self, ic, name):
        return '{:s}<{:s}>\n'.format(self.indent(ic), name)

    # vrátí název sloupce (přidá prefix pokud nějaký je)
    def getColumnName(self, prefix, number, paddingTo, padding):
        return '{:s}{:s}'.format(prefix, self.padNumber(number, paddingTo, padding));

    # vrátí koncový element sloupce
    def getColumnEndElement(self, ic, name):
        return '{:s}</{:s}>\n'.format(self.indent(ic), name)

    # vrátí hodnotu sloupce (převede metachary)
    def getColumnValue(self, ic, name):
        s = '{:s}{:s}\n'.format(self.indent(ic), name)
        return self.convertMetacharacters(s)

    # vypočítá odsazení
    def indent(self, n):
        return '    ' * n

    def padNumber(self, number, paddingTo = 0, padding = False):
        result = '{:d}'.format(number)
        if padding == True:
            result = result.zfill(paddingTo)
        return result

    def nCharPaddingRequired(self, number):
        i = 1
        while (number / 10) >= 1:
            i = i+1
            number = number / 10
        return i

    # konvertuje vybrané problémové znaky s UTF-8 kódem menším jak 128
    def convertMetacharacters(self, string):
        string = string.replace("&", "&amp;")
        string = string.replace("<", "&lt;")
        string = string.replace(">", "&gt;")
        string = string.replace('\"', "&quot;")
        string = string.replace('\r', '')
        return string

    # zkontroluje validnost názvu XML elementu
    def isValidXmlTagName(self, string):
        if  None != re.match('^[^\w:_].*$', string)  or \
            None != re.match('^[0-9].*$', string)    or \
            None != re.match('[^\w:_\.\-]', string)  :
                return False
        return

    # zkontroluje validnost obsahu XML elementu
    def isValidXmlTagValue(self, value):
        return re.match('[^\w:_.].*$', value)

    # vypíše error message na standartní chybový výstup a ukončí program se specifikovaným kódem
    def error(self, message, code = -1):
        print(message, file=sys.stderr)
        sys.exit(code)

if __name__ == "__main__":
    csv2xml = csv2xml()
    exit(0)
