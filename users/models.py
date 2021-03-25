from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.text import Truncator
from django.db.models.signals import post_save
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
import uuid
# Create your models here.

'''
delete migrations folder
python manage.py makemigrations profiles
python manage.py migrate --fake profiles zero
python manage.py migrate profiles
'''


class CustomUser(AbstractUser):
    name = models.CharField(
        db_column='name', max_length=45, blank=True)

    first_name = None
    last_name = None

    REQUIRED_FIELDS = ['email', ]  # already set in abstract model

    def __str__(self):
        if self.name is not None:
            return self.name
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = 'user'
        unique_together = ('email',)


class UserProfile(models.Model):
    id = models.SmallAutoField(primary_key=True)
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="userprofile/%Y/%m/%d/", default='user-profile.png', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
        db_table = 'user_profile'


# create the user profile is a new user created
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)


# attached a post save signal to the user model
post_save.connect(create_user_profile, sender=CustomUser)


class Product(models.Model):
    '''
    Stores Product Information
    '''

    uid = models.UUIDField(default=uuid.uuid4,
                           unique=True,
                           editable=False,
                           help_text="Unique identification number for the product."
                           )

    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             help_text="The user associated with this product.")

    name = models.CharField(max_length=256,
                            help_text="Name of the product.")

    description = models.CharField(max_length=512,
                                   blank=True,
                                   help_text="Description of the product.")

    price = models.DecimalField(max_digits=12,decimal_places=2,
                                help_text="Price of the product.")

    created = models.DateTimeField(auto_now_add=True,
                                   help_text="Date and time when the product was created in the system")

    updated = models.DateTimeField(auto_now=True,
                                   help_text="Date and time when the product was last updated in the system")

    class Meta:
        db_table = "product"
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        '''
        Returns the string representation of the product object.
        '''
        return self.name


class Order(models.Model):
    '''
    Stores Order Information
    '''

    
    uid = models.UUIDField(default=uuid.uuid4,
                           unique=True,
                           editable=False,
                           help_text="Unique idetification number for the order.")

    product_info = models.CharField(max_length=256,
                                    blank=True,
                                    help_text="Name of the order product.")

    buyer = models.ForeignKey(CustomUser,
                              related_name="order_buyer",
                              on_delete=models.CASCADE,
                              help_text="The buyer associated with the order.")

    product = models.ForeignKey(Product,
                                related_name="order_product",
                                on_delete=models.CASCADE,
                                help_text="The product of the order.")

    seller = models.ForeignKey(CustomUser,
                               related_name="order_seller",
                               on_delete=models.CASCADE,
                               help_text="The seller associated with the order.")

    created = models.DateTimeField(auto_now_add=True,
                                   help_text="Date and time when the order was created in the system")

    updated = models.DateTimeField(auto_now=True,
                                   help_text="Date and time when the order was last updated in the system")

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        '''
        Returns the string representation of the order object.
        '''
        return str(self.uid)
