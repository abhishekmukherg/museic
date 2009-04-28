"""
Content data. Currently holds Content types 
 - Text
 - Video
"""

from django.contrib.auth.models import User
from django.db import models
from djangoratings import RatingField
from django.core.files.storage import FileSystemStorage
from django.contrib.humanize.templatetags import humanize
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from museic import settings
import re
import tagging

_WHITESPACE_REGEX = re.compile(r'\W')

assert hasattr(settings, "MUSEIC_CONTENT_ROOT"), "You need to define a "\
                                "folder to store your content for MUSEIC in"
assert hasattr(settings, "MUSEIC_CONTENT_PREFIX"), "You need to define a "\
                                "prefix to get your content for MUSEIC in"
_FILE_STORAGE = FileSystemStorage(location=settings.MUSEIC_CONTENT_ROOT,
                                  base_url=settings.MUSEIC_CONTENT_PREFIX)

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
tagging.register(TextContent)

class AudioContent(Content):

    """
    Content with sound
    """

    file = models.FileField(storage=_FILE_STORAGE, upload_to="audio/%Y/%m/%d")

    def __unicode__(self):
        return mark_safe(u"""
<p id="%(slug)s">%(message)s</p>  
<script type="text/javascript">  
    AudioPlayer.embed("%(slug)s", {
        soundFile: "%(url)s",
        titles: "%(title)s",
        artists: "%(artist)s",
        autostart: "yes"
        });  
</script>
<p id="%(slug)s_download" class="download_audio">%(audio_dl)s</p>
""" % {'slug': unicode(self.slug).replace('"', ''),
        'message': _('We cannot detect your Flash player'),
        'url': self.file.url,
        'title': unicode(self.title).replace('"', ''),
        'artist': unicode(self.user).replace('"', ''),
        'audio_dl': _('Download the <a href="%s">collaboration</a>') % self.file.url,
        })

    @models.permalink
    def get_absolute_url(self):
        return ('audiocontent_details_id', [str(self.id)])
tagging.register(AudioContent)
