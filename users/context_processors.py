# users/context_processors.py
from .models import Manager, CEO

def user_role_context(request):
    if request.user.is_authenticated:
        is_manager = Manager.objects.filter(user=request.user).exists()
        is_ceo = CEO.objects.filter(user=request.user).exists()
    else:
        is_manager = False
        is_ceo = False

    return {
        'is_manager': is_manager,
        'is_ceo': is_ceo,
    }
