import PV_PCSDiffLib
comparator = PV_PCSDiffLib.ProjectComparator('test.sqlite')
comparator.readProjects('C:\\Users\\m.karabela\\Desktop\\pcs_diff\\schemat_test_1.PRO','C:\\Users\\m.karabela\\Desktop\\pcs_diff\\schemat_test_2.PRO')


# reader1 = PV_PCSDiffLib.ProjectReader('Y:\\Projekty\\!Opisy aparatur\\511_Bangalore\\Schematy\\511_schem.PRO')
# reader1.getPagesListFromFile()
# 
# dbFile = 'test.sqlite'
# tableNameA = 'Project Pages A'
# import sqlite3
# conn = sqlite3.connect(dbFile)
# c = conn.cursor()
# createstring = "CREATE TABLE '{0}'(number text, title text, lastmod text)".format(tableNameA)
# #c.execute(createstring)
# for line in reader1.pages_list:
#     #print("{0} - {1} - {2}".format(line[0], line[1], line[2]))
#     insertstring = "INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}')".format(tableNameA, line[0], line[1], line[2])
#     c.execute(insertstring)
#     conn.commit()