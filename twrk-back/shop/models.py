from PIL import Image
from django.db import models
from django.utils.translation import gettext_lazy as _

STATUS_CHOICES = [
    ('In stock', _('In stock')),
    ('On order', _('On order')),
    ('Receipt expected', _('Receipt expected')),
    ('Not available', _('Not available')),
    ('Not produced', _('Not produced')),

]


class Product(models.Model):
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

        ordering = ['title']

    title = models.CharField(_('title'), max_length=255)
    sku = models.CharField(_('sku'), max_length=255, unique=True)
    slug = models.SlugField(_('slug'), max_length=255)
    category = models.ForeignKey(verbose_name=_('category'), to='Category', on_delete=models.PROTECT,
                                 related_name='products')
    price = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="In stock")
    image = models.ImageField(_('image'), upload_to='images', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        if self.image:
            print(dir(self.image))
            im = Image.open(self.image)
            rgb_im = im.convert('RGB')
            path = F"{self.image.path.split('.')[0]}.webp"
            rgb_im.save(path, "webp")



class Category(models.Model):
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

        ordering = ['title']

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255)

    property_objects = models.ManyToManyField(verbose_name=_('properties'), to='PropertyObject')

    def __str__(self):
        return self.title


class PropertyObject(models.Model):
    class Meta:
        verbose_name = _('property object')
        verbose_name_plural = _('properties objects')

        ordering = ['title']

    class Type(models.TextChoices):
        STRING = 'string', _('string')
        DECIMAL = 'decimal', _('decimal')

    title = models.CharField(_('title'), max_length=255)
    code = models.SlugField(_('code'), max_length=255)
    value_type = models.CharField(_('value type'), max_length=10, choices=Type.choices)

    def __str__(self):
        return f'{self.title} ({self.get_value_type_display()})'


class PropertyValue(models.Model):
    class Meta:
        verbose_name = _('property value')
        verbose_name_plural = _('properties values')

        ordering = ['value_string', 'value_decimal']

    property_object = models.ForeignKey(to=PropertyObject, on_delete=models.PROTECT)

    value_string = models.CharField(_('value string'), max_length=255, blank=True, null=True)
    value_decimal = models.DecimalField(_('value decimal'), max_digits=11, decimal_places=2, blank=True, null=True)
    code = models.SlugField(_('code'), max_length=255)

    products = models.ManyToManyField(to=Product, related_name='properties')

    def __str__(self):
        return str(getattr(self, f'value_{self.property_object.value_type}', None))
