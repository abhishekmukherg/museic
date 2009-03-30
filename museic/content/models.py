"""
Content data. Currently holds Content types 
 - Text
 - Video
"""

from django.contrib.auth.models import User
from django.db import models
from djangoratings import RatingField

from django.contrib.humanize.templatetags import humanize
import re

_WHITESPACE_REGEX = re.compile(r'\W')

FIVE_STARS = [(n, u"%s stars" % unicode(humanize.apnumber(n)))
                    for n in xrange(5)]

class Content(models.Model):
    
    """
    Represents some kind of user uploaded content. This is a base class.
    Derived classes must override content(..)
    """
    
    user = models.ForeignKey(User, db_index=True)
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(editable=False, unique_for_date='pub_date')
    
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name="Publish date")
    modified_date = models.DateTimeField(auto_now=True)
    
    view_count = models.PositiveIntegerField(default=0, editable=False)
    rating = RatingField(choices=FIVE_STARS)
    
    def __repr__(self):
        return '<Content by:"%s" title:"%s">' % (self.user, self.title)
    
    def __unicode__(self):
        raise NotImplementedError

    def save(self, force_insert=False, force_update=False):
        self.slug = _WHITESPACE_REGEX.sub('_', unicode(self.title).lower())
        super(Content, self).save(force_insert, force_update)
    
    class Meta:
        abstract = True

class TextContent(Content):
    
    """
    Content that is entirely textual
    """
    
    text = models.TextField()
    
    def __unicode__(self):
        return unicode(self.text)

    @models.permalink
    def get_absolute_url(self):
        return ("textcontent_details_id", [str(self.id)])
