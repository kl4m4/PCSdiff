class ProjectReader:
    def __init__(self, projectpath):
        self.projectpath = projectpath
        self.pages_list = []
    def getPagesListFromFile(self):
        import re
        try:
            # errors='replace' po to by ignorowac znaki ktore nie sa ascii. A w niektórych projektach takie występują
            file = open(self.projectpath, 'r', errors='replace')
            file_lines = file.readlines()
        except:
            #print("Nie mogę otworzyć pliku {0}".format(filepath))
            raise
            return
        
        
        pages_list = []
        pages_count = 0
        lines_index = 0
        
        for one_line in file_lines:
            if one_line[0:7] == ".PageNo":
                try:
                    pages_count = pages_count +1
                    page_date_search = re.search('(\d)+-(\d)+-(\d)+ (\d)+:(\d)+:(\d)+', one_line)
                    page_date_string = page_date_search.group(0)
                    page_number_search = re.search('(?<=PageNo ).*(?= \d+ \'\d+-\d+)', one_line)
                    page_number_txt = page_number_search.group(0)
                    if page_number_txt[0] == '\'':
                        page_number_txt = page_number_txt[1:-1]
                    page_order_no_search = re.search('\d+(?= \'\d+-)', one_line)
                    page_order_no_text = page_order_no_search.group(0)
                    page_order_no = int(page_order_no_text)  
                    # a tytuł strony jest w następnej linijce w ".Title"
                    next_line = file_lines[lines_index+1]
                    page_title_search = re.search('(?<=.Title ).+(?= \d+)', next_line)
                    page_title = page_title_search.group(0)
                    if page_title[0] == '\'':
                        page_title = page_title[1:-1]
                    self.pages_list.append([page_number_txt, page_title, page_date_string])  
                except:
                    print("Problem z parsowaniem. Linia nr {0}".format(lines_index))
                    
            lines_index += 1
        file.close()
        
class ProjectComparator:
    def __init__(self, temp_db):
        self.dbFile = temp_db
        self.projectA = None
        self.projA_tableName = "Project A"
        self.projectB = None
        self.projB_tableName = "Project B"
    def readProjects(self, projApath, projBpath):
        self.projectAreader = ProjectReader(projApath)
        self.projectAreader.getPagesListFromFile()
        self.projectBreader = ProjectReader(projBpath)
        self.projectBreader.getPagesListFromFile()
        
        import sqlite3
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        createstring = "CREATE TABLE '{0}'(number text, title text, lastmod text)".format(self.projA_tableName)
        c.execute(createstring)
        createstring = "CREATE TABLE '{0}'(number text, title text, lastmod text)".format(self.projB_tableName)
        c.execute(createstring)
        
        for line in self.projectAreader.pages_list:
            insertstring = "INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}')".format(self.projA_tableName, line[0], line[1], line[2])
            c.execute(insertstring)
        conn.commit()
        
        for line in self.projectBreader.pages_list:
            insertstring = "INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}')".format(self.projB_tableName, line[0], line[1], line[2])
            c.execute(insertstring)
        conn.commit()
    

#filepath = 'Y:\\Projekty\\!Opisy aparatur\\511_Bangalore\\Schematy\\511_schem.PRO'

# getPagesListFromFile
# Wyciąga z pliku projektu listę stron w takim formacie:
# numer strony (użytkownika) | tytuł strony | string z daty i godziny ostatniej modyfikacji
def _getPagesListFromFile(filepath):
    import re
    try:
        # errors='replace' po to by ignorowac znaki ktore nie sa ascii. A w niektórych projektach takie występują
        file = open(filepath, 'r', errors='replace')
        file_lines = file.readlines()
    except:
        #print("Nie mogę otworzyć pliku {0}".format(filepath))
        raise
        return
    
    
    pages_list = []
    pages_count = 0
    lines_index = 0
    
    for one_line in file_lines:
        if one_line[0:7] == ".PageNo":
            try:
                pages_count = pages_count +1
                page_date_search = re.search('(\d)+-(\d)+-(\d)+ (\d)+:(\d)+:(\d)+', one_line)
                page_date_string = page_date_search.group(0)
                page_number_search = re.search('(?<=PageNo ).*(?= \d+ \'\d+-\d+)', one_line)
                page_number_txt = page_number_search.group(0)
                if page_number_txt[0] == '\'':
                    page_number_txt = page_number_txt[1:-1]
                page_order_no_search = re.search('\d+(?= \'\d+-)', one_line)
                page_order_no_text = page_order_no_search.group(0)
                page_order_no = int(page_order_no_text)  
                # a tytuł strony jest w następnej linijce w ".Title"
                next_line = file_lines[lines_index+1]
                page_title_search = re.search('(?<=.Title ).+(?= \d+)', next_line)
                page_title = page_title_search.group(0)
                if page_title[0] == '\'':
                    page_title = page_title[1:-1]
                pages_list.append([page_number_txt, page_title, page_date_string])  
            except:
                print("Problem z parsowaniem. Linia nr {0}".format(lines_index))
                
        lines_index += 1
    file.close()
    
    return pages_list

def getDifferencesByPageOrder(pagesListA, pagesListB):
    #zwraca: [nr porzadkowy strony, nr strony A, nr strony B, tytul A, tytul B, data A, data B]
    diffs = []

    
    #ustalmy ile najwiecej mamy stron
    try:
        max_pages_count = max(len(pagesListA), len(pagesListB))
    except TypeError:
        return None
        
    for index in range(0, max_pages_count-1):
        if index >= len(pagesListA)-1:
            diffs.append([index, '', pagesListB[index][0], '', pagesListB[index][1], '', pagesListB[index][2]])
            continue
        if index >= len(pagesListB)-1:
            diffs.append([index, pagesListA[index][0], '', pagesListA[index][1], '', pagesListA[index][2], ''])
            continue
        if pagesListA[index] != pagesListB[index]:
            diffs.append([index, pagesListA[index][0], pagesListB[index][0], pagesListA[index][1], pagesListB[index][1], pagesListA[index][2], pagesListB[index][2]])

    return diffs

    