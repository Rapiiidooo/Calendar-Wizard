# Calendar Wizard 2

Ceci est un script avancé du script originel 'Calendar creation wizard' for Scribus. Et il en à été inspiré, merci à Petr Vanek.
Ce script n'est pas très difficile à utiliser, vous avez quelques model initiaux, mais vous pouvez toujours utilisez vos propres création de model !

## Page 1

Selectionnez le type et choisisez le model que vous voulez. Alors vous aurez l'aperçu du model pré-selectionner puis appuyez sur 'Next'.
Vous pouvez aussi si vous en avez au préalable créer un, importer un nouveau model en cliquant sur 'Import model'.

[![N|Solid](https://cldup.com/D6_9xoBllE.png)](https://nodesource.com/products/nsolid)

## Page 2

Dans la seconde page, vous pouvez choisir le langage et les différents mois qui seront implémenté dans votre calendrier, c'est à peu près la même interface que dans le script originel de scribus.
Mais vous pouvez aussi choisir les options tels que : le numéro de la semaine, les noms complets des jours, et si vous voulez afficher les jours des mois suivants et précèdents.
Vous pouvez aussi importez un fichier ICS pour reporté sur le calendrier les journées spécial. (Cette fonctionnalité n'est malheureusement pas encore active!)


[![N|Solid](https://cldup.com/REqErZxBiM-3000x3000.png)](https://nodesource.com/products/nsolid)

## Page 3

La dernière page represente une liste de tous les éléments qui ont pu être trouvés selon le model choisi en page 1.
Vous pouvez y changer pour chacun de ses éléments la police, le style, la taille, et la couleur de la police, ainsi que la couleur des contours du cadre.

[![N|Solid](https://cldup.com/AI3lELgAlR-3000x3000.png)](https://nodesource.com/products/nsolid)

---

# **DESCRIPTION & USAGE:**

Ce script est dépendant de **Tkinter**, **lxml** et **shutil**. Normalement uniquement lxml n'est pas intégrer nativement.
Mais ce script à aussi besoin d'un model, dans le format de fichier de scribus, cela sera utile pour la génération du calendrier.
Ce script créera une interface avec différentes options activable pour la création facile d'une page de calendrier.
A la fin, vous obtiendrez un nouveau document scribus avec votre calendrier auto-générer d'après les dates que vous avez demandé.
Les positions des objets dans la page sont calculé d'après les objets du model.


## Etape pour créer un calendrier :
- 1) Choisisez un model existant ou importez en un
- 2) Cochez et cliquez sur les valeurs et option que vous voulez dans les pages 2 et 3
- 3) Appuyez 'Finnish' et le document sera auto-générer d'après le model selectionné

Il y a 4 types de calendrier supporté pour le moment:
- Year calendar with all months matrix on one page.
- Month calendar with one month matrix per page.
- Week calendar with only the week matrix per page.
- Day calendar which represent one day with hours per page.

## Etape pour créer un model de calendrier:

- 1) Créez un nouveau document scribus avec les proportions et les marge que vous voulez.
- 2) Dessinez vos texBox dans votre model.
- 3) Renomez les textBox dans les propriétés avec les noms correspondant.

Attention, les noms des objets sont extremement important, voici une liste de nom explicite qu'il reconnaît :

| Element clef | Necessité | Contient |
| ------ | ------ | ------ |
| month_box | Necessaire | Le string du mois courant |
| week_box | Necessaire | Le string de chaque jour de la semaine |
| days_box | Necessaire | Le string du nombre du jour |
| image_box | Optionel | L'image |
| num_week_box | Optionel | Le numéro de la semaine |
| name_week_box | Optionel | Le string de la colonne du numéro de la semaine |
| next_month_box | Optionel | Le string du mois suivant |
| next_week_box | Necessaire if | next_month_box| ... |
| next_days_box | Necessaire if | next_month_box | ... |
| next_image_box | Optionel | ... |
| next_num_week_box | Optionel | ... |
| next_name_week_box | Optionel | ... |
| prev_month_box | Optionel | ... |
| prev_image_box | Optionel | ... |
| prev_week_box | Necessaire | si prev_month_box |
| prev_days_box	| Necessaire | si prev_month_box |
| prev_num_week_box | Optionel | |
| next_name_week_box | Optionel | |

##### Exemple : 
[![N|Solid](https://cldup.com/8ew_xCdyM_-3000x3000.png)](https://nodesource.com/products/nsolid)

Pour le model 'year', comme l'image, ajoutez à la fin du string du nom des chiffres, à partir de 1.
Si il y a plusieurs images, faire la même chose

##### Exemple : 
    month_box1


- 4) Go to "**File**" / "**Document Setup**" / "**Information about the document**" / "**KEYWORD**" and then add the type of your calendar, and all the element name in your model :
		- **type='TheTypeOfModel'**
		"**TheTypeOfModel**" might be "**Day**" / "**Week**" / "**Month**" / "**Year**", it can be also couple of **type** like "**Month,Week**", etc.

		- **element='name_of_boxes,name_of_boxes2,name_of_boxes3'**

		##### _**Exemple :**_
			type='Month'
			element='month_box,week_box,days_box,image_box,next_month_box,next_week_box,next_days_box'



Everything is not yet well working at the moment, but I'm working on it !


##### AUTHOR:
  - **Vincent Le Jeune <vincent.ljeune@gmail.com>**

