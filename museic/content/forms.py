import museic.content.models
from django import forms
import tagging.forms


class ContentForm(forms.ModelForm):

    tags = tagging.forms.TagField()

    class Meta:
        exclude = ('user',)

    def save(self, *args, **kwargs):
        instance = super(ContentForm, self).save(*args, **kwargs)
        instance.tags = self.cleaned_data['tags']
        return instance
        

class TextContentForm(ContentForm):
    class Meta:
        model = museic.content.models.TextContent
        exclude = ('user',)


class AudioContentForm(ContentForm):
    class Meta:
        model = museic.content.models.AudioContent
        exclude = ('user',)


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50)
