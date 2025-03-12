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


class chapter(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name="分类名称")
    version = models.ForeignKey(
        version, models.SET_NULL, blank=True, null=True, verbose_name="版本"
    )

    def __str__(self):
        return self.version.title + " | " + self.name


class content(models.Model):
    title = models.CharField(max_length=10, verbose_name="标题")
    version = models.ForeignKey(
        chapter, models.SET_NULL, blank=True, null=True, verbose_name="版本/分类"
    )
    icon = models.ImageField(
        upload_to="icon/",
        default="icon/default.svg",
        blank=True,
        verbose_name="图标",
    )
    createdate = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    text = HTMLField(verbose_name="内容")

    def __str__(self):
        return self.title
