from django.db import models
from django.contrib.auth.models import User

class CitySearch(models.Model):
    """
    Модель для хранения истории поисков по городу.

    Attributes:
        user: Пользователь, который сделал поиск.
        city: Название города, по которому был сделан поиск.
        search_time: Время поиска.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    search_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Определяет наименование в интерфейсе администратора.

        Returns:
            str: "Имя пользователя - Город".
        """
        return f"{self.user.username} - {self.city}"
