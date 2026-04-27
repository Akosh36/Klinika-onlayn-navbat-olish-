from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.utils.translation import activate

class LanguageMiddleware(MiddlewareMixin):
    """Middleware to handle language based on URL prefix"""
    
    def process_request(self, request):
        # Get the current language from the URL path
        path = request.path
        language = None
        
        # Try to extract language from URL
        for lang_code, _ in settings.LANGUAGES:
            if path.startswith(f'/{lang_code}/') or path == f'/{lang_code}':
                language = lang_code
                break
        
        # If no language in URL, check session
        if not language:
            language = request.session.get('language')
        
        # If still no language, check browser language
        if not language:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE', '').split(',')[0][:2]
            # Validate it's one of our supported languages
            valid_languages = [lang[0] for lang in settings.LANGUAGES]
            if language not in valid_languages:
                language = settings.LANGUAGE_CODE
        
        # Default to English if nothing else works
        if not language:
            language = 'en'
        
        # Store language in session and activate it
        request.session['language'] = language
        request.LANGUAGE_CODE = language
        activate(language)
        
        return None
