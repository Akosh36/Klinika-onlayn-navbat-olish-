from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.conf import settings

@require_http_methods(["POST"])
def change_language(request):
    """Custom language switching view that preserves the current page"""
    language = request.POST.get('language', settings.LANGUAGE_CODE)
    
    # Validate language choice
    valid_languages = [code for code, name in settings.LANGUAGES]
    if language not in valid_languages:
        language = settings.LANGUAGE_CODE
    
    # Set the language in session
    request.session['django_language'] = language
    request.session.modified = True
    
    # Get the next URL, default to home
    next_url = request.POST.get('next', '/')
    
    # Ensure the next URL starts with the language prefix if using i18n_patterns
    if not next_url.startswith('/'):
        next_url = '/'
    
    # Add language prefix if not already present
    if not next_url.startswith(f'/{language}/') and next_url != '/':
        # Remove existing language prefix if present
        for lang_code, _ in settings.LANGUAGES:
            if next_url.startswith(f'/{lang_code}/'):
                next_url = next_url[len(f'/{lang_code}'):]
                break
        # Add the new language prefix
        next_url = f'/{language}{next_url}'
    
    response = redirect(next_url)
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        language,
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
    )
    return response
