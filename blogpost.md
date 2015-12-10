

# Backend #

npm
virtualenv
pip install django-rest-framework
django-admin startproject questions_spa


## modèles django ##
on crée une application ds notre projet avec :

    python manage.py startapp questions


### question

Le premier modèle de donnée est une question, pour faire joli, on va utiliser un index
de type slug (c'est plus sympa qu'un numéro pour réferer au question)

```python
from django.db import models
from django.utils.text import slugify


class Question(models.Model):

    # a slug used as identifier alternative to id
    slug = models.SlugField(unique=True, blank=True, editable=False)

    # text of the question
    question = models.TextField()

    # date when this question was posted
    created = models.DateTimeField(auto_now_add=True)


    # overide save to generate the slug on save
    def save(self, *args, **kwargs):

        if( not self.slug) :
            self.slug = slugify(self.question)

        super(Question, self).save(*args, **kwargs)

```

On le rajoute de même à l'admin ce qui nous permettra de peupler la base de données,

```
from django.contrib import admin
from .models import Question
# Register your models here.

@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    pass

```
Ajouter l'application questions à la liste des applications installées dans le settings.py (INSTALLED_APPS)
On valide et on crée la base de données avec:

   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver


ouvrir localhost:8000/admin/ avec le login fourni à la commande createsuperuser

- réponse
## exposing with django-rest-framework ##

## ajouter des exemples, et tester ##

# Frontend #

## boilerplate et installation

- création du dossier /frontend/
- bower gulp
- gulp compile -> /static/
- servir par défault index.html:
```python
  url(r'^$', staticfiles.views.serve, kwargs={"path":"index.html"}),
```
