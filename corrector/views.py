import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .utils import TextCorrector

corrector_service = TextCorrector()

@ensure_csrf_cookie
def index(request):
    """Renders main interface."""
    return render(request, 'corrector/index.html')

def correct_api(request):
    """API endpoint for dynamic real-time text correction."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            result = corrector_service.correct_text(text)
            return JsonResponse({'status': 'success', 'data': result})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)