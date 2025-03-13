from django.db import models
from tinymce.models import HTMLField


class version(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name="名称")
    title_jp = models.CharField(max_length=30, unique=True, verbose_name="日语")
    sub = models.CharField(max_length=15, unique=True, verbose_name="索引")
    release_date = models.DateField(verbose_name="发售时间")
    url = models.URLField(default="", blank=True, verbose_name="官网")
    enable = models.BooleanField(default=False, verbose_name="启用")
    cover = models.ImageField(
        upload_to="cover/", null=True, blank=True, verbose_name="封面图"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "游戏版本"
        verbose_name_plural = "游戏版本"


class content(models.Model):
    title = models.CharField(max_length=20, verbose_name="标题")
    createdate = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    lastmodified = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    text = HTMLField(blank=True, verbose_name="内容")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "攻略内容"
        verbose_name_plural = "攻略内容"


class to(models.Model):
    title = models.CharField(max_length=20, default="", blank=True, verbose_name="标题")
    icon = models.FileField(
        upload_to="icon/",
        default="icon/seedling.svg",
        blank=True,
        verbose_name="图标",
    )
    version = models.ForeignKey(
        version, models.SET_NULL, null=True, blank=True, verbose_name="版本"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="分类",
    )
    link = models.ForeignKey(
        content, models.SET_NULL, null=True, blank=True, verbose_name="攻略内容"
    )
    enable = models.BooleanField(default=True, verbose_name="启用")
    page = models.CharField(
        max_length=50,
        default="",
        blank=True,
        verbose_name="特殊页面",
        help_text="组件路径",
    )
    sort = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="排序",
    )

    def __str__(self):
        if self.version != None:
            if self.parent == None:
                if self.link == None:
                    return str(self.version.title + " | " + self.title)
                else:
                    return str(self.version.title + " | " + self.link.title)
            else:
                if self.link == None:
                    return str(self.version.title + " | " + self.parent.title + " | " + self.title)
                else:
                    return str(self.version.title + " | " + self.parent.title + " | " + self.link.title)
        else:
            return f"ERROR - {str(self.id)}"

    class Meta:
        verbose_name = "攻略索引"
        verbose_name_plural = "攻略索引"
