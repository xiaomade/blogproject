from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=128,verbose_name='博客分类')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="博客分类"
        verbose_name_plural="博客分类"

class Tag(models.Model):

    name = models.CharField(max_length=128, verbose_name='博客标签')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "博客标签"
        verbose_name_plural = '博客标签'

class Post(models.Model):
    title=models.CharField(max_length=128,verbose_name="文章标题")
    author=models.ForeignKey(User,verbose_name="博客作者",on_delete=models.CASCADE)
    img=models.ImageField(upload_to='blog_images',null=True,blank=True,verbose_name='博客配图')
    body = models.TextField(verbose_name='博客正文')
    abstract = models.TextField(max_length=256, blank=True, null=True, verbose_name='博客摘要')
    visiting = models.PositiveIntegerField(default=0, verbose_name='博客访问量')
    category = models.ForeignKey(Category,verbose_name="博客分类",on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', verbose_name='博客标签')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):

        return self.title

    def increase_visiting(self):
        self.visiting += 1
        self.save(update_fields=['visiting'])

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self,*args,**kwargs):
        if not self.abstract:
            md=markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.abstract=strip_tags(md.convert(self.body))[:54]
        super(Post,self).save(*args,**kwargs)


    class Meta:
        ordering=['-created_time']
        verbose_name='博客'
        verbose_name_plural='博客'







    