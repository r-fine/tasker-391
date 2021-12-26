from django.urls import reverse
from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from mptt.models import MPTTModel, TreeForeignKey

from ckeditor.fields import RichTextField


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
    description = RichTextField(
        verbose_name='Service Description',
        blank=True,
        null=True,
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

    @property
    def average_review(self):
        reviews = ReviewRating.objects.filter(
            service=self, status=True).aggregate(average=models.Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(round(reviews['average'], 2))
        return avg

    @property
    def count_review(self):
        reviews = ReviewRating.objects.filter(
            service=self, status=True).aggregate(count=models.Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    @property
    def is_root(self):
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
    summary = RichTextField(blank=True, null=True)
    pricing = RichTextField(blank=True, null=True)
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
    one, two, three, four, five = 1, 2, 3, 4, 5
    RATINGS = (
        (one, 1),
        (two, 2),
        (three, 3),
        (four, 4),
        (five, 5),
    )
    service = models.ForeignKey(
        Service,
        related_name='review_service',
        on_delete=models.CASCADE,
        null=True
    )
    service_option = models.ManyToManyField(
        ServiceOption,
        verbose_name='Review for',
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
    review = RichTextField(
        config_name='minimal',
        verbose_name='Review Details',
        max_length=500,
        blank=True,
        null=True,
    )
    rating = models.IntegerField(choices=RATINGS, default=five)
    status = models.BooleanField(
        verbose_name='Review Visibility',
        default=True
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.subject
