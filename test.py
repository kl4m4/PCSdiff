import PV_PCSDiffLib
import configparser

config = configparser.ConfigParser()
config.read('.\\test cases\\testcases.ini')

for case in config.sections():
    if config[case]['active'] == 'True':
        print("===============================")
        print("Test case: \'{0}\'".format(case))
        print(config[case]['desc'])
        print("Test files:")
        print(config[case]['fileA'])
        print(config[case]['fileB'])
        
    
        comparator = PV_PCSDiffLib.ProjectComparator(':memory:')
        comparator.readProjects('.\\test cases\\'+config[case]['fileA'], '.\\test cases\\'+config[case]['fileB'])
        comparator.compare()
        print("Comparator print output:>>>")
        comparator.prettyPrint()
        print("<<< end")
    
