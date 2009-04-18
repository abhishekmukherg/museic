import museic.content.models
from django.forms import ModelForm

class ContentForm(ModelForm):
    class Meta:
        exclude = ('user',)

class TextContentForm(ContentForm):
    class Meta:
        model = museic.content.models.TextContent
        exclude = ('user',)

class AudioContentForm(ContentForm):
    class Meta:
        model = museic.content.models.AudioContent
        exclude = ('user',)
