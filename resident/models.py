from django.db import models
from tinymce.models import HTMLField
from index.models import version

SEX_CHOICES = [
    ("M", "男"),  # Male
    ("F", "女"),  # Female
    ("O", "其他"),  # Other
    ("U", "未知"),  # Unknown
]

SEASON = [
    ("SPR", "春"),  # Spring
    ("SUM", "夏"),  # Summer
    ("AUT", "秋"),  # Autumn
    ("WIN", "冬"),  # Winter
    ("N", "无"),  # None
]

CLASSIFICATION = [
    ("G", "花嫁候补"),  # Boy
    ("B", "花婿候补"),  # Girl
    ("O", "普通居民"),  # Ordinary
    ("E", "精灵"),  # Elf
]

class resident(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name="名字")
    name_jp = models.CharField(max_length=10, unique=True, verbose_name="名字（日语）")
    name_en = models.CharField(max_length=20, unique=True, verbose_name="名字（英语）")
    form = models.CharField(
        max_length=1, choices=CLASSIFICATION, default="O", verbose_name="分类"
    )
    version = models.ForeignKey(
        version, models.SET_NULL, default=9, null=True, blank=True, verbose_name="版本"
    )
    icon = models.ImageField(
        upload_to="icon/mineraltown/",
        blank=True,
        verbose_name="头像",
    )
    photo = models.ImageField(
        upload_to="photo/mineraltown/",
        blank=True,
        verbose_name="全身",
    )
    note = HTMLField(blank=True, verbose_name="注释")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "居民"
        verbose_name_plural = "居民"
