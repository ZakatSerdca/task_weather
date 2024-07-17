≡  Описание выполненного задания:
## Сделано:
- Написаны тесты
- Сделаны автодополнения при вводе
- Предложения по просмотру ранее запрашеваемых мест
- Сохранение истории поиска
### Технологии:
- [Django 5.0.7](https://docs.djangoproject.com/en/5.0/ "Перейти")
- [Django REST framework 3.15.2](https://www.django-rest-framework.org/ "Перейти")
- [Poetry](https://python-poetry.org/docs/ "Перейти")
 
### Использованные API:
- Информация о погоде и геокодированние (получение иформации о координатах из названия города): [Open-Meteo](https://open-meteo.com/)

#### Взаимствования:
 _Следующие части из HTML файлов были написаны с помошью AI:_

home.html

```javascript
$(document).ready(function() {
    var $input = $("input[name='city']");
    var $container = $("#autocomplete-container");

    $input.on('input', function() {
        var query = $(this).val();
        if (query.length > 2) {
            $.ajax({
                url: "{% url 'city_autocomplete' %}",
                data: {
                    'query': query
                },
                success: function(data) {
                    $container.empty();
                    $.each(data.suggestions, function(index, suggestion) {
                        $container.append('<div class="autocomplete-suggestion">' + suggestion + '</div>');
                    });

                    $(".autocomplete-suggestion").on('click', function() {
                        $input.val($(this).text());
                        $container.empty();
                    });
                }
            });
        } else {
            $container.empty();
        }
    });
});
```

