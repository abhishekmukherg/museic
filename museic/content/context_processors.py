import museic.content.forms

def login_form(request):
    return {'search_form': museic.content.forms.SearchForm()}

