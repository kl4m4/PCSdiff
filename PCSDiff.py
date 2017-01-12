import PV_PCSDiffLib
import sys

if len(sys.argv) != 3:
    print(sys.argv)
    print("Sposób użycia:\nPCSDiff plik1 plik2")
else:
    
    pathA = sys.argv[1]
    pathB = sys.argv[2]
    
    comparator = PV_PCSDiffLib.ProjectComparator(':memory:')
    comparator.readProjects(pathA, pathB)
    comparator.compare()
    comparator.prettyPrint()