#Calendar Wizard 2


## Page 1

The first window, is where you have the choice of the _* type *_ of your calendar. The _* type *_ means, what will appear by page of your calendar, it can be a day, a week, a month, or a year.
The next step is the model, there are corolation between _* type *_ and _* model *_. The model of *day*, can not be the same as *year*. There are different _*model*_ per _* type *_.
You have got the preview to see what will be created. And you can import your own _*model*_ if you have made one. _All models are scribus files_.

## Page 2

In the second window you can choose the language and the different month, which will be implements to your calendar, this is the same as Calendar Wizard 2.
But you can also choose if there is the number of the week, if you want the right full name of the day, and if you wanna show the days before and after the current month.
You can also import an ICS file to match with special days.

## Page 3

The last page integrate all elements that can be found and customisable by the users :
**
month_string
week_string
week_number
day_string
day_number
day_saturday
day_sunday
day_holidays
**
There are a Fonts family panel : For any of these elements you can change the font, the font size, and the color.


/* 
expliquer le rôle des templates, dire qu'on utilise des templates :

Les templates que l'on utilise sont des documents scribus vierge, le nom des boites-objets que l'on attribut est très important, 
car notre plugin associe ces boîtes-objets à des caractéristiques particulière, celle que l'utilisateur aura choisi.  
*/


HOW TO CREATE A NEW MODEL


Particular name :
{
	year model :
	{
		image = image_box
		boite de légende = caption_box
	}
	month model :
	{
		image = image_box
		boite du mois en cours = month_box
		boite des jours de la semaine = week_box
		boite des numéros de jours = days_box
		boite des numéros de semaine = num_week_box
		//boite de légende = caption_box

		boite du mois suivant = next_month_box
		image = next_image_box
		boite des jours de la semaine = next_week_box
		boite des numéros de jours = next_days_box
		boite des numéros de semaine = next_num_week_box

		boite du mois precedent = prev_month_box
		image = prev_image_box
		boite des jours de la semaine = prev_week_box
		boite des numéros de jours = prev_days_box
		boite des numéros de semaine = prev_num_week_box
	}
	week model :
	{
		image = image_box
	}
	day model :
	{
		image = image_box
	}
}
