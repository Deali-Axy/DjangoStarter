from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from datetime import date

# Create your views here.
def index(request):
    """
    Demo Dashboard / Landing Page
    """
    context = {
        'title': 'Demo Dashboard',
        'breadcrumbs': [
            {'text': 'Home', 'url': '/'},
            {'text': 'Demo', 'url': None, 'icon': 'fa-solid fa-layer-group'},
        ],
        'stats': [
            {'label': 'Total Movies', 'value': '1,284', 'change': '+12%', 'icon': 'fa-solid fa-film', 'color': 'blue'},
            {'label': 'Active Actors', 'value': '842', 'change': '+5%', 'icon': 'fa-solid fa-user-group', 'color': 'green'},
            {'label': 'Albums Sold', 'value': '45.2k', 'change': '+28%', 'icon': 'fa-solid fa-compact-disc', 'color': 'purple'},
            {'label': 'Avg Rating', 'value': '4.8', 'change': '+2%', 'icon': 'fa-solid fa-star', 'color': 'yellow'},
        ]
    }
    return render(request, 'demo/index.html', context)

def styleguide(request):
    """
    UI/UX Style Guide and Component Library
    """
    context = {
        'title': 'Design System',
        'breadcrumbs': [
            {'text': 'Demo', 'url': reverse('demo:index'), 'icon': 'fa-solid fa-layer-group'},
            {'text': 'Style Guide', 'url': None, 'icon': 'fa-solid fa-palette'},
        ]
    }
    return render(request, 'demo/styleguide.html', context)

def movies(request):
    """
    Movie Catalog Demo (Grid Layout)
    """
    # Mock data for visualization
    movies_data = [
        {'title': 'Inception', 'year': 2010, 'rating': 9.3, 'genre': 'Sci-Fi', 'image': 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=500&q=80'},
        {'title': 'The Dark Knight', 'year': 2008, 'rating': 9.5, 'genre': 'Action', 'image': 'https://images.unsplash.com/photo-1509347528160-9a9e33742cd4?auto=format&fit=crop&w=500&q=80'},
        {'title': 'Interstellar', 'year': 2014, 'rating': 9.1, 'genre': 'Adventure', 'image': 'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&w=500&q=80'},
        {'title': 'Pulp Fiction', 'year': 1994, 'rating': 9.2, 'genre': 'Crime', 'image': 'https://images.unsplash.com/photo-1594909122845-11baa439b7bf?auto=format&fit=crop&w=500&q=80'},
        {'title': 'Dune', 'year': 2021, 'rating': 8.8, 'genre': 'Sci-Fi', 'image': 'https://images.unsplash.com/photo-1541963463532-d68292c34b19?auto=format&fit=crop&w=500&q=80'},
        {'title': 'Blade Runner 2049', 'year': 2017, 'rating': 8.9, 'genre': 'Sci-Fi', 'image': 'https://images.unsplash.com/photo-1542204165-65bf26472b9b?auto=format&fit=crop&w=500&q=80'},
    ]
    
    context = {
        'title': 'Movies',
        'breadcrumbs': [
            {'text': 'Demo', 'url': reverse('demo:index'), 'icon': 'fa-solid fa-layer-group'},
            {'text': 'Movies', 'url': None, 'icon': 'fa-solid fa-film'},
        ],
        'movies': movies_data
    }
    return render(request, 'demo/movies.html', context)

def actors(request):
    """
    Actors Directory Demo (List/Table Layout)
    """
    actors_data = [
        {'name': 'Leonardo DiCaprio', 'role': 'Lead Actor', 'country': 'USA', 'status': 'Available', 'avatar': 'https://i.pravatar.cc/150?u=leo'},
        {'name': 'Brad Pitt', 'role': 'Lead Actor', 'country': 'USA', 'status': 'Busy', 'avatar': 'https://i.pravatar.cc/150?u=brad'},
        {'name': 'Margot Robbie', 'role': 'Lead Actress', 'country': 'Australia', 'status': 'Available', 'avatar': 'https://i.pravatar.cc/150?u=margot'},
        {'name': 'Cillian Murphy', 'role': 'Lead Actor', 'country': 'Ireland', 'status': 'On Set', 'avatar': 'https://i.pravatar.cc/150?u=cillian'},
    ]

    context = {
        'title': 'Actors',
        'breadcrumbs': [
            {'text': 'Demo', 'url': reverse('demo:index'), 'icon': 'fa-solid fa-layer-group'},
            {'text': 'Actors', 'url': None, 'icon': 'fa-solid fa-users'},
        ],
        'actors': actors_data
    }
    return render(request, 'demo/actors.html', context)

def music(request):
    """
    Music Player Demo (Complex Interface)
    """
    albums_data = [
        {'title': 'Random Access Memories', 'artist': 'Daft Punk', 'year': 2013, 'cover': 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?auto=format&fit=crop&w=300&q=80'},
        {'title': 'The Dark Side of the Moon', 'artist': 'Pink Floyd', 'year': 1973, 'cover': 'https://images.unsplash.com/photo-1619983081563-430f63602796?auto=format&fit=crop&w=300&q=80'},
        {'title': 'Thriller', 'artist': 'Michael Jackson', 'year': 1982, 'cover': 'https://images.unsplash.com/photo-1605020420620-20c943cc4669?auto=format&fit=crop&w=300&q=80'},
    ]

    context = {
        'title': 'Music Library',
        'breadcrumbs': [
            {'text': 'Demo', 'url': reverse('demo:index'), 'icon': 'fa-solid fa-layer-group'},
            {'text': 'Music', 'url': None, 'icon': 'fa-solid fa-music'},
        ],
        'albums': albums_data,
        'now_playing': {
            'title': 'Instant Crush',
            'artist': 'Daft Punk ft. Julian Casablancas',
            'duration': '5:37',
            'progress': 65
        }
    }
    return render(request, 'demo/music.html', context)

def htmx_test(request):
    """
    HTMX CSRF Test Page
    """
    if request.method == "POST":
        from django.utils import timezone
        import time
        # Simulate a small delay to show the loading state
        time.sleep(0.5)
        return render(request, 'demo/partials/htmx_response.html', {
            'time': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'message': 'HTMX Request Successful!'
        })
    
    context = {
        'title': 'HTMX Test',
        'breadcrumbs': [
            {'text': 'Demo', 'url': reverse('demo:index'), 'icon': 'fa-solid fa-layer-group'},
            {'text': 'HTMX Test', 'url': None, 'icon': 'fa-solid fa-bolt'},
        ]
    }
    return render(request, 'demo/htmx.html', context)

def sse_demo(request):
    """
    Server-Sent Events (SSE) Demo Page
    """
    context = {
        'title': 'SSE Chat Demo',
        'breadcrumbs': [
            {'text': 'Demo', 'url': reverse('demo:index'), 'icon': 'fa-solid fa-layer-group'},
            {'text': 'SSE Chat', 'url': None, 'icon': 'fa-solid fa-comments'},
        ]
    }
    return render(request, 'demo/sse-demo.html', context)

def test_403(request):
    raise PermissionDenied()

def test_404(request):
    # Django handles 404 automatically, but here we return the template explicitly for demo purposes
    return render(request, '404.html', status=404)

def test_500(request):
    # Trigger a real 500 for demo purposes
    raise Exception("This is a test 500 error!")
