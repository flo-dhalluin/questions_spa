from __future__ import unicode_literals
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


    def __str__(self):
        return "Question : %s"%self.slug
