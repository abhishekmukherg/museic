import django.contrib.auth
def login_form(request):
    return {'login_form': django.contrib.auth.forms.AuthenticationForm()}

