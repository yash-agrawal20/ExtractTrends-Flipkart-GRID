from django.db import models

# Create your models here.
class Instadata(models.Model):
    profile_id = models.CharField(primary_key=True, max_length=30)
    image_url = models.CharField(db_column='image_URL', max_length=500, blank=True, null=True)  # Field name made lowercase.
    score = models.FloatField(blank=True, null=True)
    cat = models.CharField(max_length=30, blank=True, null=True)
    sub_cat = models.CharField(max_length=30, blank=True, null=True)
    kwords = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instadata'