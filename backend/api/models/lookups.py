from django.db import models

class OrganSystem(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'Organ System'
        verbose_name_plural = '__add_organ_system'

    def __str__(self):
        return self.name
    

class StaffUploader(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'Uploading staff'
        verbose_name_plural = '__add_uploading_staff'

    def __str__(self):
        return self.name