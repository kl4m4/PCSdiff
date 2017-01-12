import PV_PCSDiffLib
import os
import configparser

config = configparser.ConfigParser()
config.read('.\\test cases\\testcases.ini')

for case in config.sections():
    if config[case]['active'] == 'True':
        print("===============================")
        print("Przypadek testowy \'{0}\'".format(case))
        print(config[case]['desc'])
        print("Testowe pliki projektow:")
        print(config[case]['fileA'])
        print(config[case]['fileB'])
        print("\n")
    
        comparator = PV_PCSDiffLib.ProjectComparator(':memory:')
        comparator.readProjects('.\\test cases\\'+config[case]['fileA'], '.\\test cases\\'+config[case]['fileB'])
        comparator.compare()
        comparator.printDiff()
    
