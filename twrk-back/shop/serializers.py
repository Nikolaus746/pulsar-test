import glob

from rest_framework import serializers
from .models import STATUS_CHOICES


class IMGField(serializers.Field):
    """
    image objects are serialized into specific notation.
    """

    def to_representation(self, value):
        if value:
            path = value.path.split('.')[0]
            files = glob.glob(F"{path}.*")
            format = list(map(lambda x: x.split('.')[-1], files))
            img = {
                "path": value.url.split('.')[0],
                "formats": format
            }

            return img

        else:
            return None

class ProductSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_blank=True, max_length=255)
    sku = serializers.CharField(required=False, allow_blank=True, max_length=255)
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, default='In stock')
    image = IMGField()


