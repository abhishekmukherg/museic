import museic.content.forms

def search_form(request):
    return {'search_form': museic.content.forms.SearchForm()}

