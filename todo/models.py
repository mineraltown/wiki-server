from django.db import models
from index.models import version
from tinymce.models import HTMLField
from django.core.validators import MinValueValidator, MaxValueValidator

SEASON = [
    ("SPR", "春"),  # Spring
    ("SUM", "夏"),  # Summer
    ("AUT", "秋"),  # Autumn
    ("WIN", "冬"),  # Winter
]


class festival(models.Model):
    version = models.ForeignKey(
        version, models.SET_NULL, default=9, null=True, blank=True, verbose_name="版本"
    )
    name = models.CharField(max_length=20, verbose_name="名称")
    month = models.CharField(
        max_length=3, choices=SEASON, default="SPR", verbose_name="月"
    )
    day = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(31)],
        default=1,
        verbose_name="日",
    )
    start_time = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="开始时间"
    )
    end_time = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="结束时间"
    )
    address = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="地点"
    )
    note = HTMLField(blank=True, verbose_name="注释")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "节日"
        verbose_name_plural = "节日"
