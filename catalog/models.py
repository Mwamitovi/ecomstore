# catalog/models.py
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class ActiveCategoryManager(models.Manager):
    """ Manager class
        to return only those categories where each instance is active
    """
    def get_queryset(self):
        return super(ActiveCategoryManager, self)\
            .get_queryset().filter(is_active=True)


@python_2_unicode_compatible
class Category(models.Model):
    """ Model class containing information about
        a category in the product catalog
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=50, unique=True,
        help_text='Unique value for product page URL, created from name.'
    )
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(
        "Meta Keywords", max_length=255,
        help_text='Comma-delimited set of SEO keywords for meta tag.'
    )
    meta_description = models.CharField(
        "Meta Description", max_length=255,
        help_text='Content for description meta tag.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # default Category Manager
    objects = models.Manager()
    # Active Category Manager
    active = ActiveCategoryManager()

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    # @models.permalink
    def get_absolute_url(self):
        # return 'catalog_category', (), {'category_slug': self.slug}
        return reverse(
            'catalog:catalog_category',
            kwargs={'category_slug': self.slug}
        )


class ActiveProductManager(models.Manager):
    """ Manager class
        to return only those products where each instance is "active"
    """
    def get_queryset(self):
        return super(ActiveProductManager, self)\
            .get_queryset().filter(is_active=True)


class FeaturedProductManager(models.Manager):
    """ Manager class
        to return only those products where each instance is "featured"
    """
    def get_queryset(self):
        return super(FeaturedProductManager, self)\
            .get_queryset().filter(is_active=True).filter(is_featured=True)


@python_2_unicode_compatible
class Product(models.Model):
    """ Model class containing information about a product;
        instances of this class are what the user adds to their
        shopping cart and can subsequently purchase
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(
        max_length=255, unique=True,
        help_text='Unique value for product page URL, created from name.'
    )
    brand = models.CharField(max_length=50)
    sku = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    old_price = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, default=0.00
    )
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField()
    description = models.TextField()
    meta_keywords = models.CharField(
        max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag.'
    )
    meta_description = models.CharField(
        max_length=255, help_text='Content for description meta tag'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)

    # image fields added later, require varchar(100) as set in the db
    image = models.ImageField(upload_to='images/products/main')
    thumbnail = models.ImageField(upload_to='images/products/thumbnails')
    image_caption = models.CharField(max_length=200)

    # default Product Manager
    objects = models.Manager()
    # Active Product Manager
    active = ActiveProductManager()
    # Featured Product Manager
    featured = FeaturedProductManager()

    # Added a store location
    location = models.CharField(max_length=50, default='Kampala-Kasubi')

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        permissions = (
            ("kasubi_store", "Based at Kasubi Store"),
        )

    def __str__(self):
        return self.name

    # @models.permalink
    def get_absolute_url(self):
        # return 'catalog_product', (), {'product_slug': self.slug}
        return reverse(
            'catalog:catalog_product',
            kwargs={'product_slug': self.slug}
        )

    @property
    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    # usually purchased with this product...
    def cross_sells(self):
        """ Gets other Product instances that
            have been combined with the current instance in past orders.
            Includes any orders placed by anonymous users that haven't registered
        """
        from checkout.models import Order, OrderItem
        orders = Order.objects.filter(orderitem__product=self)
        order_items = OrderItem.objects.filter(order__in=orders).exclude(product=self)
        products = Product.active.filter(orderitem__in=order_items).distinct()
        return products

    # users who purchased this product also bought....
    def cross_sells_user(self):
        """ Gets other Product instances that were ordered by
            other registered customers who also ordered the current instance.
            Uses all past orders of each registered customer, and
            not just the order in which the current instance was purchased
        """
        # noinspection PyUnresolvedReferences
        from checkout.models import Order, OrderItem
        from django.contrib.auth.models import User
        users = User.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter(order__user__in=users).exclude(produc=self)
        products = Product.active.filter(orderitem__in=items).distinct()
        return products

    def cross_sells_hybrid(self):
        """ Gets other Product instances that were both combined with
            the current instance in orders placed by unregistered customers,
            and also all products that were ordered by registered customers
        """
        from checkout.models import Order, OrderItem
        from django.contrib.auth.models import User
        from django.db.models import Q
        orders = Order.objects.filter(orderitem__product=self)
        users = User.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter(
            Q(order__in=orders) | Q(order__user__in=users)
        ).exclude(product=self)
        products = Product.active.filter(orderitem__in=items).distinct()
        return products


class ActiveProductReviewManager(models.Manager):
    """ Manager class to return only those product reviews where
        each instance is approved
    """
    def all(self):
        return super(ActiveProductReviewManager, self).all().filter(is_approved=True)


class ProductReview(models.Model):
    """ model class containing product review data associated
        with a product instance
    """
    RATINGS = (
        (5, 5), (4, 4), (3, 3), (2, 2), (1, 1),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(default=5, choices=RATINGS)
    is_approved = models.BooleanField(default=True)
    content = models.TextField()
    # default ProductReview Manager
    objects = models.Manager()
    # Approved ProductReview Manager
    approved = ActiveProductReviewManager()
