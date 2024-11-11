from django.db import models


# Create your models here.
class Breed(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название породы",
        help_text="Введите название породы",
    )
    description = models.TextField(
        verbose_name="Описание породы",
        help_text="Введите описание породы",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "породы"

    def __str__(self):
        return self.name


class Dog(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Кличка собаки", help_text="Введите кличку собы"
    )
    breed = models.ForeignKey(
        Breed,
        on_delete=models.SET_NULL,
        verbose_name="Порода",
        help_text="Введите породу собы",
        blank=True,
        null=True,
        related_name="dogs",
    )
    photo = models.ImageField(
        upload_to="dogs/photo",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите фото собы",
    )
    date_born = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения",
        help_text="Введите дату рождения собы",
    )

    class Meta:
        verbose_name = "Соба"
        verbose_name_plural = "Собы"
        ordering = ["breed", "name"]

    def __str__(self):
        return self.name
