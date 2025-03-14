from django.db import models
from tinymce.models import HTMLField
from django.core.validators import MinValueValidator, MaxValueValidator

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
]

CLASSIFICATION = [
    ("G", "花嫁候补"),  # Boy
    ("B", "花婿候补"),  # Girl
    ("O", "普通居民"),  # Ordinary
    ("E", "精灵"),  # Elf
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

    name = models.CharField(max_length=10, unique=True, verbose_name="名字")
    name_jp = models.CharField(max_length=10, unique=True, verbose_name="名字（日语）")
    name_en = models.CharField(max_length=10, unique=True, verbose_name="名字（英语）")
    form = models.CharField(
        max_length=1, choices=CLASSIFICATION, default="O", verbose_name="分类"
    )
    icon = models.ImageField(
        upload_to="icon/saikai/",
        blank=True,
        verbose_name="头像",
    )
    photo = models.ImageField(
        upload_to="photo/saikai/",
        blank=True,
        verbose_name="全身",
    )
    desc = HTMLField(blank=True, verbose_name="描述")
    first = models.CharField(max_length=10, default="最初", verbose_name="登场")
    address = models.CharField(max_length=10, verbose_name="地址")
    sex = models.CharField(
        max_length=1, choices=SEX_CHOICES, default="M", verbose_name="性别"
    )
    birth_month = models.CharField(
        max_length=3, choices=SEASON, default="SPR", verbose_name="生日（月）"
    )
    birth_day = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)],
        default=1,
        verbose_name="生日（日）",
    )
    birth_day_another = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        default=0,
        verbose_name="生日（日）与主角冲突",
    )
    family = models.CharField(
        max_length=50, default="", blank=True, verbose_name="家庭成员"
    )
    like = models.JSONField(default=like_default, verbose_name="喜好")
    trip = HTMLField(blank=True, verbose_name="行程")
    note = HTMLField(blank=True, verbose_name="注释")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "居民"
        verbose_name_plural = "居民"


EVENT_CLASSIFICATION = [
    ("E", "年度节日"),  # Event
    ("R", "居民事件"),  # Resident
    ("M", "婚后事件"),  # Marriage
    ("O", "其他事件"),  # Other
]


class event(models.Model):
    title = models.CharField(max_length=20, unique=True, verbose_name="事件名称")
    form = models.CharField(
        max_length=1, choices=EVENT_CLASSIFICATION, default="O", verbose_name="分类"
    )
    desc = HTMLField(blank=True, verbose_name="描述")
    month = models.CharField(
        max_length=3,
        choices=SEASON,
        default="SPR",
        verbose_name="月",
        help_text="年度节日专用",
    )
    day = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        default=0,
        verbose_name="日",
        help_text="年度节日专用",
    )
    date = models.CharField(max_length=20, default="-", blank=True, verbose_name="日期")
    week = models.CharField(max_length=20, default="-", blank=True, verbose_name="星期")
    time = models.CharField(max_length=30, default="-", blank=True, verbose_name="时间")
    weather = models.CharField(
        max_length=10, default="晴", blank=True, verbose_name="天气"
    )
    address = models.CharField(
        max_length=20, default="", blank=True, verbose_name="场所"
    )
    other = HTMLField(blank=True, verbose_name="其他")
    performer = models.ManyToManyField(resident, blank=True, verbose_name="登场居民")
    result = HTMLField(blank=True, verbose_name="结果")
    note = HTMLField(blank=True, verbose_name="注释")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "事件"
        verbose_name_plural = "事件"


FISH_PROBABILITY = [
    (0, "无"),
    (1, "低"),
    (2, "高"),
]


class fish(models.Model):

    def location_list():
        return {
            "海边": True,
            "湖边": False,
            "泉水": False,
            "上游": False,
            "下游": False,
            "池塘": False,
            "温泉": False,
            "地底湖": False,
        }

    name = models.CharField(max_length=10, unique=True, verbose_name="名称")
    name_jp = models.CharField(max_length=10, unique=True, verbose_name="名称（日语）")
    level = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        default=1,
        verbose_name="蓄力等级",
    )
    spring = models.PositiveSmallIntegerField(
        choices=FISH_PROBABILITY, default=2, verbose_name="春"
    )
    summer = models.PositiveSmallIntegerField(
        choices=FISH_PROBABILITY, default=2, verbose_name="夏"
    )
    autumn = models.PositiveSmallIntegerField(
        choices=FISH_PROBABILITY, default=2, verbose_name="秋"
    )
    winter = models.PositiveSmallIntegerField(
        choices=FISH_PROBABILITY, default=2, verbose_name="冬"
    )
    location_list = models.JSONField(default=location_list, verbose_name="地点")
    max_size = models.PositiveSmallIntegerField(verbose_name="最大尺寸")
    min_size = models.PositiveSmallIntegerField(verbose_name="最小尺寸")
    king = models.BooleanField(default=False, verbose_name="鱼王")
    special = models.BooleanField(default=False, verbose_name="特殊")
    trash = models.BooleanField(default=False, verbose_name="垃圾")
    note = models.CharField(max_length=100, default="", blank=True, verbose_name="注释")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "钓鱼"
        verbose_name_plural = "钓鱼"


class cookbook(models.Model):

    def default():
        return [""]

    name = models.CharField(max_length=20, unique=True, verbose_name="名称")
    name_jp = models.CharField(max_length=20, unique=True, verbose_name="名称（日语）")
    price = models.PositiveIntegerField(verbose_name="出售价格")
    physical = models.PositiveSmallIntegerField(verbose_name="回复体力")
    fatigue = models.PositiveSmallIntegerField(verbose_name="回复疲劳")
    ingredients = models.JSONField(default=default, verbose_name="成分")
    kitchenware = models.JSONField(default=default, verbose_name="厨具")
    how_to_get = models.CharField(
        max_length=100, default="", blank=True, verbose_name="获得方法"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "料理"
        verbose_name_plural = "料理"
