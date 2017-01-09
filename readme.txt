Zapytanie zwracajace listê wszystkich ró¿nic przy za³o¿eniu ¿e porównujemy strony za pomoc¹ ich tytu³ów: tzn zmiana tytu³u = jedna strona ubywa, druga siê pojawia.
Ogólnie:
SELECT(
	SELECT ró¿niceAB
	UNION
	SELECT ró¿niceBA
)
ORDER BY...

Ró¿nice sprawdzamy przez LEFT OUTER JOIN, bo CROSS JOIN nie jest zaimplementowane w sqlite.
Kod:
SELECT * FROM (
SELECT 'Project A'.number as numA, 'Project A'.title as titleA, 'Project A'.lastmod as dateA, 'Project B'.number as numB, 'Project B'.title as titleB, 'Project B'.lastmod as dateB 
FROM 'Project A' LEFT OUTER JOIN 'Project B' 
ON 'Project A'.title = 'Project B'.title 
WHERE dateA <> dateB OR dateA IS NULL OR dateB IS NULL
UNION
SELECT 'Project A'.number as numA, 'Project A'.title as titleA, 'Project A'.lastmod as dateA, 'Project B'.number as numB, 'Project B'.title as titleB, 'Project B'.lastmod as dateB 
FROM 'Project B' LEFT OUTER JOIN 'Project A' 
ON 'Project A'.title = 'Project B'.title 
WHERE dateA <> dateB OR dateA IS NULL OR dateB IS NULL
)
ORDER BY numA ASC

Pozostaje problem z sortowaniem, bo nie dzia³a