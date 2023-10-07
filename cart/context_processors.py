from .cart import Cart


def cart(request):
    """Добавляем корзину в контекст проекта"""
    return {"cart": Cart(request)}
