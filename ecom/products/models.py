from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.ImageField(upload_to='category_icons/')  # Assuming you are using an ImageField for icon

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    icon = models.ImageField(upload_to='subcategory_icons/')  # Assuming you are using an ImageField for icon

    def __str__(self):
        return self.name
