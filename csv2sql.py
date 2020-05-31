# Auteur : Rioche Patrick   le 18/05/2020
#
# Mode d'emploi :
#
#   csv2sql.py critereimpact.csv >createcritereimpact.sql
#
#   Ce programme genere le chargement de la table en sql a partir
#   d'un export csv
#
#   Entree :
#       tablexcel.csv   fichier texte creer pour excel
#
#   Sortie :
#       NA
#
#   Version :
#       V1.0    18/05/2020
#
__version__ = 'V1.0'
DEBUG = 1

import os, sys

if len(sys.argv) == 1:
    print ( "Mode de d'emploi : " + __version__ )
    print ( "                                 " )
    print ( "    csv2sql.py tablexcel.csv" )
    sys.exit(1)

#
#   Recuperation des arguments de la ligne de commande
#
sFic = sys.argv[1]
#sFic = 'C:/Users/Rioche-P/Google Drive/00-PERSO-CG/00-FORMD-CG/GIT/CSV2SQL/critereimpact.csv'
sTable = sFic.split("/")[-1].split(".")[0]

#
#   Initialisation global
#
dDicoSql = {}

#
#   Definition des fonctions
#

def ClearString( sTheString ):
    sS1 = sTheString.lstrip().rstrip()
    sS2 = sS1.replace(' ',' ')
    sS3 = sS2.replace('(',' ')
    sS4 = sS3.replace(')',' ')    
    sS5 = sS4.replace(',',' ')
    sS6 = sS5.replace('\'',' ')
    sS7 = sS6.replace('û','u')
    sS8 = sS7.replace('é','e')
    sS9 = sS8.replace('è','e')
    sSA = sS9.replace('à','a')
    sSB = sSA.replace('ç','c')
    return( sSB )
    
def AddDicoRubSql( sRub, nPos ):
    dDicoSql["rub:" + str(nPos)] = ClearString( sRub )

def AddDicoIteSql( sIte,  nIte, nPos ):
    dDicoSql["ite:" + str(nIte) + ":pos:" + str(nPos)] = ClearString( sIte )

def AddDicoNbRubSql( nNbRub ):
    dDicoSql["nbrub:"] = str(nNbRub) 

def AddDicoNbItemSql( nNbIte ):
    dDicoSql["nbite:"] = str(nNbIte) 
    
#
#   Ouverture du fichier doc_rptObjects.txt
#
nLigne = 0
nTable = 0

if ( DEBUG ): print( "sFic : " + sFic + "<" )

fI = open(sFic, "r")

for sLigne in  fI.readlines():
    #
    #   Selection des noms des tables
    #
    if nLigne == 0:
        #
        #   Ligne des declarations des rubriques de la table
        #
        if ( DEBUG ): print( "1 :>" + sLigne + "<" )
        nRub = 1
        for sRub in sLigne.split(";"):
            AddDicoRubSql( sRub, nRub ) 
            nRub = nRub + 1
            
        AddDicoNbRubSql( nRub - 1 )
    else:
        if ( DEBUG ): print( "N :>" + sLigne + "<" )
        nPos = 1
        for sIte in sLigne.split(";"):
            AddDicoIteSql( sIte, nLigne, nPos ) 
            nPos = nPos + 1

    nLigne = nLigne + 1
    if ( DEBUG ): print( "Nombre de ligne : " + str(nLigne) )

fI.close()

AddDicoNbItemSql( nLigne - 1 )

if ( DEBUG ): print( dDicoSql )


#
#   Restitution en create table
#
print( "create table " + str(sTable) + " (" ),
sMaxRub = dDicoSql["nbrub:"]
r = 1
while( r < int(sMaxRub)+1 ):
    if ( r == 1 ):
        #
        print( dDicoSql["rub:" + str(r)] + " integer primary key" ),
    else:
        #    
        print( dDicoSql["rub:" + str(r)] + " varchar(50)" ),
    if ( r < int(sMaxRub) ):
        print( "," ),
    r = r + 1

print( ");" )

#
#   Restitution en insert into
#
sMaxIte = dDicoSql["nbite:"]
i = 1
while( i < int(sMaxIte)+1 ):
    print( "insert into " + str(sTable) + " (" ),
    sMaxRub = dDicoSql["nbrub:"]
    r = 1
    while( r < int(sMaxRub)+1 ):
        print( dDicoSql["rub:" + str(r)] ),
        if ( r < int( sMaxRub ) ):
            print( "," ),
        r = r + 1

    print( ") " ),
    #
    r = 1
    print( " values ( " ),
    while( r < int(sMaxRub)+1 ):
        print( "'" + dDicoSql["ite:" + str(i) + ":pos:" + str(r) ] + "'" ),
        if ( r < int( sMaxRub ) ):
            print( "," ),
        r = r + 1

    print( ");" )
    
    i = i + 1

#
#   Fin csv2sql.py
#
