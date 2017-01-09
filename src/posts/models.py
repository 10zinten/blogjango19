from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from markdown_deux import markdown
import urllib

from comments.models import Comment
# Create your models here.
# MVC MODEL VIEW CONTROLLER


#Post.objects.all()
#Post.objects.create(user=user, title="Some time")
class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		##Post.objects.all() = super(PostManager, self).all()
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=120) 
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to=upload_location,
							  null=True, 
							  blank=True, 
							  height_field="height_field", 
							  width_field="width_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __unicode__(self):
		return self.title

	def __str__(self):
		return	self.title

	objects = PostManager()	

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"slug": self.slug})
		#return "/posts/%s/" %(self.id)	

	class Meta:
		ordering = ["-timestamp", "-updated"]	

	def get_markdown(self):
		content = self.content
		markdown_text = markdown(content)
		if "http" in markdown_text:
			markdown_text = markdown_duex_url_decoder(markdown_text)
		return mark_safe(markdown_text)

	@property
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(instance)
		return qs	


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

def markdown_duex_url_decoder(markdown_text):
	markdown_text_list = markdown_text.split("\"")
	encoded_url = markdown_text_list[1]
	decoded_url = urllib.unquote(encoded_url).decode('utf8')
	markdown_text_list[1] = decoded_url
	return "\"".join(markdown_text_list)


pre_save.connect(pre_save_post_receiver, sender=Post)


