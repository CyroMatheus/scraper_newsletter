from django.db import models

class Tag(models.Model):
    tag = models.CharField(max_length=225, unique=True)
    model = models.CharField(
        max_length=50,
        choices = [
            ('0','JornalGrandeBahia'), 
            ('1','LfNews'), 
            ('2','VilasMagazine'), 
            ('3','BurburinhoNews'), 
            ('4','BahiaNoAr'),
            ('5','RelataBahia'),
        ]
    )
    
    def __str__(self):
        return "{}".format(self.tag)

class Category(models.Model):
    category = models.CharField(max_length=225, unique=True)
    model = models.CharField(
        max_length=50,
        choices = [
            ('0','JornalGrandeBahia'), 
            ('1','LfNews'), 
            ('2','VilasMagazine'), 
            ('3','BurburinhoNews'), 
            ('4','BahiaNoAr'),
            ('5','RelataBahia'),
        ]
    )

    def __str__(self):
        return "{}".format(self.category)

class Post(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    date = models.DateField()
    text = models.TextField()
    model = models.CharField(
        max_length=25,
        default="",
        choices=[
            ('0', 'JornalGrandeBahia'),
            ('1', 'LfNews'),
            ('2', 'VilasMagazine'),
            ('3', 'BurburinhoNews'),
            ('4', 'BahiaNoAr'),
            ('5','RelataBahia'),
        ] 
    )
    categories = models.ManyToManyField(Category, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')

    def __str__(self):
        return "{} {}".format(self.date, self.title)
