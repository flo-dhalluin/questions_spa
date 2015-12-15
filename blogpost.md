

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

django-rest-framework, il nous faut créer l'api que notre application va utiliser
pour afficher les question posée. Nous allons implémenter la première qui récupère la liste des questions.

Il nous faut implémenter 2 choses, un Serializer (transforme les objects accessible par l'API ici le modèle Question, en dictionnaire python et inversement), et une classe de vue surchargeant la class APIView, qui transforme ce dictionnaire en format demandé, sur une route donnée.

django-rest-framework fournit des supers classes qui marchent *très* bien avec les modèles djangos (et pour cause..)

```python
from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('slug', 'created', 'question')

```

pour les vues, ajouter la classe QuestionListView dans le views.py de l'applicatoin.
Nous allons utiliser la class ListCreateAPIView, qui permet de lister, et de créer un nouveau modèle (via POST).

```python

from rest_framework import generics
from .serializers import QuestionSerializer
from .models import Question

class QuestionListView(generics.ListCreateAPIView):
    model = Question
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

```

rajoutons la vue ainsi crée dans les urls.
```
urlpatterns = patterns('',
                       url(r'^$', QuestionListView.as_view(), name='question-list'),
                       )

dans le main urls   
 url(r'^q/', include('questions.urls')),
```

## ajouter des exemples, et tester ##


   curl http://localhost:8000/q/  -> un bon json de la liste des questions ! YAY


# Frontend #


## le début 
Ok, curl n'est pas vraiment user friendly, et puis je vous ai alleché avec Polymer.

L'idée d'une single page app est de vraiment découpler le frontend de la partie api.

On va donc coder notre appli web dans un dossier séparé, appellons le au hasard, "frontend"
dans ce dossier :

     > npm init
     > npm install bower gulp --save-dev
     > bower install --save Polymer/polymer#^1.2.0

on va créer notre page d'index vide avec dedans, attention :
```html
<!DOCTYPE html>
<html>
  <head>
    <title> Django Question SinglePage </title>
    <script src="static/bower_components/webcomponentsjs/webcomponents-lite.min.js"></script>
  </head>

  <body>
    <h1> It works </h1>
  </body>
</html>
```

et la servir en ajoutant à question_spa\urls.py, la vue :
```python
  url(r'^$', staticfiles.views.serve, kwargs={"path":"index.html"}),
```

et spécifer à django que des fichiers statiques se trouvent dans ledit dossier frontend en ajoutant à settings.py :
```
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "frontend"),
]
```

vas'y, va voir un peu sur localhost:8000, c'est bon ? 

## notre premier element polymer, une liste de question

## gulp ! 

