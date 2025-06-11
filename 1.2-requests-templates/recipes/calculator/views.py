from django.shortcuts import render, reverse

INGREDIENTS = {
    'omelet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'sandwich': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    }
}


DISH_NAMES = {
    'omelet': 'омлет',
    'pasta': 'паста',
    'sandwich': 'бутерброд'
}


def home_view(request):
    template_name = 'calculator/home.html'
    pages = dict()
    for dish in INGREDIENTS.keys():
        pages[DISH_NAMES.get(dish, dish).title()] = f'{dish}/?amount=1'
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def recipe(request, dish):
    amount = int(request.GET.get('amount', 1))
    ingredients = {ingredient: round(base_amount * amount, 2) for ingredient, base_amount in INGREDIENTS[dish].items()}

    pages = {
        'Домашняя страница': reverse('home')
    }
    context = {
        'recipe': ingredients,
        'dish': DISH_NAMES.get(dish, dish),
        'amount': amount,
        'pages': pages
    }

    result = render(request, 'calculator/index.html', context)
    return result
