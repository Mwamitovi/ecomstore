# cart/management/commands/delete_old_carts.py
from django.core.management.base import BaseCommand
from cart import cart


class Command(BaseCommand):
    help = "Delete shopping cart items more than SESSION_COOKIE_DAYS days ago"

    @staticmethod
    def handle_noargs(**options):
        cart.remove_old_cart_items()
