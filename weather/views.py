import requests
from django.shortcuts import render
from .forms import CityForm
from .models import CitySearch
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def home(request):
    """Функция с логикой главной страницы. Декоратор чекает авторизацию пользователя и аутентифицирует.

    Параметры:
        request (HttpRequest): Объект запроса HTTP.

    Returns:
        HttpResponse: Рендер ответ HTTP с прогнозом и историей поиска
    """
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data["city"]
            user = request.user

            CitySearch.objects.create(user=user, city=city)

            weather_data = get_weather_data(city)

            context = {
                "form": form,
                "weather_data": weather_data,
            }
            return render(request, "weather/home.html", context)
    else:
        form = CityForm()

    # История поиска пользователя
    search_history = CitySearch.objects.filter(user=request.user).order_by(
        "-search_time"
    )
    context = {
        "form": form,
        "search_history": search_history,
    }
    return render(request, "weather/home.html", context)


def get_weather_data(city):
    """Функция для получения прогноза погоды по городу.

    Параметры:
        city (str): Название города.

    Returns:
        dict: Словарь с данными о прогнозе погоды.
    """

    # Название города --> координаты
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geocode_response = requests.get(geocode_url)
    geocode_data = geocode_response.json()

    if "results" in geocode_data and geocode_data["results"]:
        location = geocode_data["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]

        # Прогноз погоды
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        return {
            "city": location["name"],
            "latitude": latitude,
            "longitude": longitude,
            "temperature": weather_data["current_weather"]["temperature"],
        }
    return None


def city_autocomplete(request):
    """Функция для автозаполнения при вводе названия города

    Параметры:
        request (HttpRequest): Объект запроса HTTP.

    Returns:
        JsonResponse: Спмсок подсказок (может быть пустым).
    """
    query = request.GET.get("query", "")
    if query:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}"
        response = requests.get(url)
        data = response.json()
        suggestions = (
            [city["name"] for city in data["results"]] if "results" in data else []
        )
        return JsonResponse({"suggestions": suggestions})
    return JsonResponse({"suggestions": []})
