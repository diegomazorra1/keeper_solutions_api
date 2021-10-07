from django.db import models

from keeper_solution_backend_test import settings


class BookMark(models.Model):
    """
    User BookMark manager
    """
    title = models.CharField(
        max_length=120, unique=True, verbose_name="Título")
    url = models.URLField(
        max_length=500, verbose_name="Url")
    create_at = models.DateField('Fecha de Creación',
                                 auto_now=False, auto_now_add=True)
    is_public = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Marcador"
        ordering = ['user']

    def __str__(self):
        return self.title
