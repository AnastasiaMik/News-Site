from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.utils.timezone import now

class LinkVoteCountManager(models.Manager):
    def get_query_set(self):
        return super(LinkVoteCountManager, self).get_query_set().annotate(
            votes=Count('vote')).order_by('-rank_score', '-votes')

class Link(models.Model):
    title = models.CharField("Headline", max_length=100) #заголовок, который виден всем
    submitter = models.ForeignKey(User) #посетитель - внешний ключ в базе данных
    submitted_on = models.DateTimeField(auto_now_add=True) #при почещении сайта дата/время ставится автоматически
    rank_score = models.FloatField(default=0.0) #оценка, которая ставится новости
    url = models.URLField("URL", max_length=250, blank=True) #позволяет передавать каждой новости ссылку на ее источник
    description = models.TextField(blank=True) #позволяет добавлять к новости какое-либо описание
    with_votes = LinkVoteCountManager() #подсчет кол-ва голосов
    objects = models.Manager()

    def __unicode__(self): #передает строковое значение модели
        return self.title
    def get_absolute_url(self):
        return reverse("link_detail", kwargs={"pk": str(self.id)})
    def set_rank(self):
        SECS_IN_HOUR = float(60*60)
        GRAVITY = 1.2

        delta = now() - self.submitted_on
        item_hour_age = delta.total_seconds() // SECS_IN_HOUR
        votes = self.votes - 1
        self.rank_score = votes / pow((item_hour_age+2), GRAVITY)
        self.save()

class Vote(models.Model):
    voter = models.ForeignKey(User)
    link = models.ForeignKey(Link)

    def __unicode__(self):
        return "%s upvoted %s" % (self.voter.username, self.link.title)

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    about_youself = models.TextField(null=True)

    def __unicode__(self):
        return "%s's profile" % self.user

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)
