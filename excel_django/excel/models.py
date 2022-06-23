from django.db import models

class Document(models.Model):

    content = models.FileField(verbose_name="ファイル",upload_to="file/")

