from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class LanguageMiddleware(MiddlewareMixin):
    """Middleware to handle language based on URL prefix"""
    
    def process_request(self, request):
        # Get the current language from the URL path
        path = request.path
        language = 'uz'  # default
        
        for lang_code, _ in settings.LANGUAGES:
            if path.startswith(f'/{lang_code}/') or path == f'/{lang_code}':
                language = lang_code
                break
        
        # Store language in session
        request.session['language'] = language
        request.LANGUAGE_CODE = language
        
        return None
