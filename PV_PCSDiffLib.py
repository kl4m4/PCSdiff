import sqlite3
#import terminaltables

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
    def __init__(self, temp_db_file):
        self.dbFile = temp_db_file
        self.dbConn = None
        self.projectA = None
        self.projectB = None
        self.compareResult = None
    def ___del___(self):
        self.dbConn.close()
    def readProjects(self, projApath, projBpath):
        self.projectAreader = ProjectReader(projApath)
        self.projectAreader.getPagesListFromFile()
        self.projectBreader = ProjectReader(projBpath)
        self.projectBreader.getPagesListFromFile()
        
        self.dbConn = sqlite3.connect(self.dbFile)
        c = self.dbConn.cursor()
        createstring = "CREATE TABLE 'Project A'(number text, title text, lastmod text)"
        c.execute(createstring)
        createstring = "CREATE TABLE 'Project B'(number text, title text, lastmod text)"
        c.execute(createstring)
        
        for line in self.projectAreader.pages_list:
            insertstring = "INSERT INTO 'Project A' VALUES ('{0}', '{1}', '{2}')".format(line[0], line[1], line[2])
            c.execute(insertstring)
        self.dbConn.commit()
        
        for line in self.projectBreader.pages_list:
            insertstring = "INSERT INTO 'Project B' VALUES ('{0}', '{1}', '{2}')".format(line[0], line[1], line[2])
            c.execute(insertstring)
        self.dbConn.commit()
        
    def compare(self):
        queryString = "SELECT * FROM (SELECT 'Project A'.number as numA, 'Project A'.title as titleA, 'Project A'.lastmod as dateA, 'Project B'.number as numB, 'Project B'.title as titleB, 'Project B'.lastmod as dateB FROM 'Project A' LEFT OUTER JOIN 'Project B' ON 'Project A'.number = 'Project B'.number WHERE dateA <> dateB OR dateA IS NULL OR dateB IS NULL UNION SELECT 'Project A'.number as numA, 'Project A'.title as titleA, 'Project A'.lastmod as dateA, 'Project B'.number as numB, 'Project B'.title as titleB, 'Project B'.lastmod as dateB FROM 'Project B' LEFT OUTER JOIN 'Project A' ON 'Project A'.number = 'Project B'.number WHERE dateA <> dateB OR dateA IS NULL OR dateB IS NULL) ORDER BY numA ASC"
        c = self.dbConn.cursor()
        try:
            self.compareResult = c.execute(queryString)
        except:
            raise
            return
        
    def prettyPrint(self):
        print("Projekt A: {0}\nProjekt B: {1}".format(self.projectAreader.projectpath, self.projectBreader.projectpath))
        print("Zmiany:")
        print("{0:>7} {1:>7} {2:<70} {3:<20}".format('projekt', '#', 'Tytuł strony', 'Data modyfikacji'))
        for line in self.compareResult:
            print("{0:>7} {1:>7} {2:<70} {3:<20}".format('A',str(line[0]),str(line[1]),str(line[2])))
            print("{0:>7} {1:>7} {2:<70} {3:<20}".format('B',str(line[3]),str(line[4]),str(line[5])))
            print("----------------------------------------------------------------------------------------------------------")
      
    def printDiff(self):
        #print("Project A: {0}".format(self.projectAreader.projectpath))
        #print("Project B: {0}\n".format(self.projectBreader.projectpath))
        for line in self.compareResult:
            print(line)
	
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

    
