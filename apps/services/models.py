from django.urls import reverse
from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.postgres.indexes import GinIndex


class Service(MPTTModel):
    name = models.CharField(
        verbose_name='Service Name',
        max_length=255,
        unique=True,
        db_index=True,
    )
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    description = models.TextField(
        verbose_name='Service Description',
        blank=True
    )
    image = models.ImageField(
        upload_to="images/",
        default="images/500_500.png"
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'Services'
        indexes = [
            GinIndex(
                name='GinIndex', fields=['name'], opclasses=['gin_trgm_ops']
            ),
        ]

    def get_absolute_url(self):
        return reverse('services:service_detail', args=[self.slug])

    def edit_url(self):
        return reverse('accounts:edit_service', args=[self.pk])

    def delete_url(self):
        return reverse('accounts:delete_service', args=[self.pk])

    def averageReview(self):
        reviews = ReviewRating.objects.filter(
            service=self, status=True).aggregate(average=models.Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(
            service=self, status=True).aggregate(count=models.Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    @property
    def is_parent(self):
        if self.level == 0:
            return True
        else:
            return None

    def __str__(self):
        if self.level == 0:
            return f'{self.name} (Root)'
        else:
            return f'- {self.name}'


class ServiceOption(models.Model):
    service = models.ForeignKey(
        Service,
        related_name='service',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(verbose_name='Service Option Name', max_length=255)
    summary = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="images/",
        default="images/500_500.png"
    )
    is_active = models.BooleanField(
        verbose_name="Service Option Visibility",
        default=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            GinIndex(
                name='NewGinIndex', fields=['name'], opclasses=['gin_trgm_ops']
            ),
        ]

    def edit_url(self):
        return reverse('accounts:edit_service_option', args=[self.pk])

    def delete_url(self):
        return reverse('accounts:delete_service_option', args=[self.pk])

    def __str__(self):
        return self.name


class ReviewRating(models.Model):
    service = models.ForeignKey(
        Service,
        related_name='review_service',
        on_delete=models.CASCADE,
        null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='review_user',
        on_delete=models.CASCADE
    )
    subject = models.CharField(
        verbose_name='Review Title',
        max_length=100,
        blank=True
    )
    review = models.TextField(
        verbose_name='Review Details',
        max_length=500,
        blank=True
    )
    rating = models.IntegerField()
    status = models.BooleanField(
        verbose_name='Review Visibility',
        default=True
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
