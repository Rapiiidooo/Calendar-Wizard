# -*- coding: utf-8 -*-
#!/usr/bin/env python

from lxml import etree
import re
import glob,os

model='calendar222.sla'
type_ele=re.compile('element=\'(.*)\'')
tree = etree.parse(model)
keys = tree.getroot()
for key in keys:
    val=key.attrib['KEYWORDS']
str1=re.findall(type_ele,val)
str2=re.split(",",str1[0])
print(str2) 


mon_type='year'
models_path='.'
    
type_cal=re.compile('type=\'.*' + mon_type + '.*\'')

# On cherche dans le repertoire avec les modeles

available_models=[]
#On parcours tous les documents qui se terminent par .sla dans le
#repertoire qui contient les modeles
for model in os.listdir(models_path):
    if model.endswith(".sla"):

#On parse chaque modele pour voir quels sont les keywords definis
        tree = etree.parse(model)
        keys = tree.getroot()
        for key in keys:
            val=key.attrib['KEYWORDS']

#Si on trouve un type de calendrier dans les KEYWORDS du document
#on recupere ce modele pour l'afficher dans l'etape suivante
            avail=re.findall(type_cal,val)
            if avail:
                available_models.append(model)

print available_models

    Contact GitHub API Training Shop Blog About 


