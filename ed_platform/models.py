from django.db import models


class CourseModel(models.Model):
    '''Модель курса. Связана с :model: "users.CustomUser - создатель экземпляра модели"'''

    name = models.CharField(max_length=100, verbose_name="Название курса", unique=True)
    preview = models.ImageField(
        upload_to="ed_platform/courses", verbose_name="Превью", null=True, blank=True
    )
    description = models.TextField(max_length=1000, verbose_name="Описание")
    owner = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        name="owner",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Курс: {self.name}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class LessonModel(models.Model):
    """Модель урока. Связана с :model: users.CustomUser - создатель экземпляра, :model: ed_platform.CourseModel -
    курс к которому относится урок"""

    name = models.CharField(max_length=100, verbose_name="Название урока")
    description = models.TextField(max_length=1000, verbose_name="описание")
    preview = models.ImageField(
        upload_to="ed_platform/lessons/", verbose_name="Превью", blank=True, null=True
    )
    video_url = models.URLField(blank=True, null=True)
    course = models.ForeignKey(
        CourseModel,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="курс",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        name="owner",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Урок: {self.name}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class SubscriptionModel(models.Model):
    """Модель подписки пользователя на курс. Связана с :model: users.CustomUser - пользовательс активной подпиской,
    :model: ed_platform.CourseModel - курс, на который подписан пользователь."""

    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, name="user")
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE, name="course")
