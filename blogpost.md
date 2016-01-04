

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

Nous allons a présent afficher la liste des questions au lieu de notre message pas vraiment informatif.

Nous allons pour cela créer un élément Polymer correspondant à une liste de question.

créons le dossier frontend/elements/ qui contiendra nos éléments polymer
et le fichier frontend/elements/question-list.html

```html

<link rel="import"
      href="/static/bower_components/polymer/polymer.html">
<link rel="import"
      href="/static/bower_components/iron-ajax/iron-ajax.html">

<dom-module id="question-list">
  <template>
    
    <h1> Questions </h1>
    
    <!-- hardcoded url to our REST api view
         the result of the query is bound to this component "questions" variable -->
    <iron-ajax
       auto
       url="/q/"
       handle-as="json"
       last-response="{{questions}}"
       debounce-duration="300">
    </iron-ajax>

    <ul>
    <template is="dom-repeat" items="[[questions]]">
	<li>
	  {{item.question}}
	</li>
    </template>
    </ul>
  </template>
  
  <script>
      Polymer({
      is:"question-list",
      ready: function() {
         this.questions = []; /* start empty */
         console.log("hello le monde, ici question-list");
      },
      });
      
  </script>
</dom-module>
```

Nous constatons que notre élément réutilise un élément existant, qui fait partie de polymer : iron-ajax qui nous permet de faire une requête ajax. Les éléments de la collection "iron" sont des éléments de base. Nous verrons plus tard la collection "material" qui permet de styler. 
nous l'installons avec bower :

	bower install --save PolymerElements/iron-ajax



nous modifions le fichier index.html pour afficher l'élément
```html
<!DOCTYPE html>
<html>
  <head>
    <title> Django Question SinglePage </title>
    <script src="static/bower_components/webcomponentsjs/webcomponents-lite.min.js"></script>
	<!-- on importe notre nouvel élément ici : -->
    <link rel="import" href="static/elements/question-list.html">

  </head>

  <body>
	<!-- coucou toi ! -->
    <question-list></question-list>
  </body>
</html>
```

Allez, on lance un petit runserver, et on ouvre la page / .. go, ouvre les outils de débug et vérifie que le message "hello le monde" apparaît dans la console et qu'on a effectivement une requête ajax vers /q/ ! 

## stylage et utilisation des elements paper

installons les éléments iron-flex-layout (pour faire un layout à base de flexbox, penser grille css mais en mieux..), et les éléments paper necessaires.

```
bower install --save PolymerElements/iron-flex-layout
bower install --save PolymerElements/paper-toolbar
bower install PolymerElements/paper-header-panel
```

modifions index.html
```
    <link rel="import"
      href="/static/bower_components/paper-header-panel/paper-header-panel.html">
    <link rel="import"
	  href="/static/bower_components/paper-toolbar/paper-toolbar.html">

  </head>

  <body class="layout fullbleed vertical">
    <paper-header-panel class="flex">
      <paper-toolbar>
	<div> Questions </div>
      </paper-toolbar>
      <question-list></question-list>
    </paper-header-panel>
  </body>
```

là, c'est tout joli avec une belle barre d'outils, tout occupe bien l'écran.

## Poser une question

La vue générique ListeCreateAPIView de rest-framework expose normalement 2 api. Une répondant au requête de type GET, qui liste les instances existantes et une répondant aux requêtes POST qui permet de créer une nouvelle instance. Testons :

```
curl -X POST -d question="Est-ce que ça marche" http://localhost:8000/q/
```

Vérifions sur notre navigateur web, une nouvelle question a bien été prise en compte !



## gulp ! 

