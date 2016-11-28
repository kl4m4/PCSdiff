

#filepath = 'Y:\\Projekty\\!Opisy aparatur\\511_Bangalore\\Schematy\\511_schem.PRO'

# getPagesListFromFile
# Wyciąga z pliku projektu listę stron w takim formacie:
# numer strony (użytkownika) | tytuł strony | string z daty i godziny ostatniej modyfikacji
def getPagesListFromFile(filepath):
    import re
    file = open(filepath, 'r')
    file_lines = file.readlines()
    
    pages_list = []
    pages_count = 0
    lines_index = 0
    
    for one_line in file_lines:
        if one_line[0:7] == ".PageNo":
            #print(one_line)
            pages_count = pages_count +1
            
            page_date_search = re.search('(\d)+-(\d)+-(\d)+ (\d)+:(\d)+:(\d)+', one_line)
            page_date_string = page_date_search.group(0)
            page_number_search = re.search('(?<=PageNo ).*(?= \d+ \'\d+-\d+)', one_line)
            page_number_txt = page_number_search.group(0)
            if page_number_txt[0] == '\'':
                page_number_txt = page_number_txt[1:-1]
            page_order_no_search = re.search('\d+(?= \'\d+-)', one_line)
            page_order_no_text = page_order_no_search.group(0)
            #print("nr porzadkowy = {0}; numer zakladki = {1}; data = {2}".format(page_order_no_text, page_number_txt, page_date_string))
            page_order_no = int(page_order_no_text)  
            next_line = file_lines[lines_index+1]
            page_title_search = re.search('(?<=.Title ).+(?= \d+)', next_line)
            page_title = page_title_search.group(0)
            if page_title[0] == '\'':
                    page_title = page_title[1:-1]
            pages_list.append([page_number_txt, page_title, page_date_string])            
        lines_index += 1
    file.close()
    
    return pages_list

def getDifferenecesByPageOrder(pagesListA, pagesListB):
    #zwraca: [nr porzadkowy strony, nr strony A, nr strony B, tytul A, tytul B, data A, data B]
    diffs = []
    
    # ustalmy ile najwiecej mamy stron
    max_pages_count = max(len(pagesListA), len(pagesListB))
    for index in range(0, max_pages_count-1):
        if index > len(pagesListA):
            diffs.append([index, '', pagesListB[index][0], '', pagesListB[index][1], '', pagesListB[index][2]])
            continue
        if index > len(pagesListB):
            diffs.append([index, pagesListA[index][0], '', pagesListA[index][1], '', pagesListA[index][2], ''])
            continue
        #print("data A = {0}, data B = {1}".format(pagesListA[index][2], pagesListB[index][2]))
        if pagesListA[index] != pagesListB[index]:
            print("roznica!")
            diffs.append([index, pagesListA[index][0], pagesListB[index][0], pagesListA[index][1], pagesListB[index][1], pagesListA[index][2], pagesListB[index][2]])
    print("-")
    return diffs

    