import pdfplumber
import pandas as pd
import os



def extract_tables_with_pdfplumber(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:

            for table in page.extract_tables():
                # puste tabele na koncu strony itp
                if table == [['', '', '']] or table == [['', '']] or table == [['']] or table == []:
                    continue
                # exception kiedy table[1] - kolumn nie da sie ustawic bo to jest wrapowana tabela 
                # na dwie strony
                try:
                    # Zakladamy, ze tabela ma tytul na gorze, potem ma nazwy kolumn i potem ma 
                    # wszystkie wiersze 
                    # 
                    # Tak jest zawsze oprocz 2 przypadkow
                    # - na górze tabela listy hostów, zaczyna się od nazw kolumn
                    # - kontynuacja tabeli na następnej stronie
                    # 
                    # W tym przypadku, celowo ignoruję tabelę z listą hostów na górze.
                    # filtered_list = [item for item in table[0] if item is not None]
                    cleaned_list = [[element for element in sublist if element not in [None, '']] for sublist in table]
                    if len(cleaned_list[0]) > 1:
                        # mozesz tu wyprintowac filtered_list, w tym miejscu jest jakis problem
                        # z parsowaniem, czesto sie to zdarza na koncowkach stron
                        # kiedy merge sie nie uda
                        #
                        # print(filtered_list)
                        break
                    df = {"name": cleaned_list[0][0], "columns": cleaned_list[1], "tables": cleaned_list[2:]}
                    tables.append(df)
                except:
                    cleaned_list = [[element for element in sublist if element not in [None, '']] for sublist in table]
        
                    # przypadek kiedy tabela sie wrapuje na nastepna strone
                    tables[-1]["tables"] += cleaned_list

                # df = pd.DataFrame(table[2:], columns=table[1])
    return tables

# Usage
for pdf_path in os.listdir():
    if not pdf_path.endswith(".pdf"):
        continue
    tables = extract_tables_with_pdfplumber(pdf_path)
    f = open('output.txt','w',  encoding="utf-8")

    print(pdf_path, file=f)
    # sys.stdout = f
    # Display the tables
    for i, table in enumerate(tables):
        if table["name"] != "Informacje ogólne" and table["name"] != "Interfejsy sieciowe":
            continue

        # Tabele informacyjne i sieciowe sa inne niz standard, nie maja nazw kolumn
        table["tables"].append(table["columns"])
        table["columns"] = None

        for i, x in enumerate(table["tables"]):
            if len(x) == 0:
                continue            
            x[0] = x[0].replace(":", "")
        # # if table.contains
        print(f"Table {i+1}", file=f)
        # print(table)
        print(table, file=f)
    # print(tables, file=f)
    
