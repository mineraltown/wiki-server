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
    ("G", "花嫁候补"),  # Girl
    ("B", "花婿候补"),  # Boy
    ("O", "普通居民"),  # Ordinary
    ("T", "其他居民"),  # Other
    ("E", "小矮人"),  # Elf
]


class resident(models.Model):

    def like_default():
        return {
            "最喜欢": ["", ""],
            "很喜欢": ["", ""],
            "喜欢": ["", ""],
            "普通": ["", ""],
            "讨厌": ["", ""],
            "很讨厌": ["", ""],
        }

    name = models.CharField(max_length=10, verbose_name="名字")
    name_jp = models.CharField(max_length=10, verbose_name="名字（日语）")
    name_en = models.CharField(max_length=20, verbose_name="名字（英语）")
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
    sex = models.CharField(
        max_length=1, choices=SEX_CHOICES, default="M", verbose_name="性别"
    )
    birth_month = models.CharField(
        max_length=3, choices=SEASON, default="SPR", verbose_name="生日（月）"
    )
    birth_day = models.PositiveSmallIntegerField(default=1, verbose_name="生日（日）")
    birth_day_another = models.PositiveSmallIntegerField(
        default=0, verbose_name="生日（日）与主角冲突"
    )
    like = models.JSONField(default=like_default, blank=True, verbose_name="喜好")
    note = HTMLField(blank=True, verbose_name="注释")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "居民"
        verbose_name_plural = "居民"
