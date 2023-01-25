from decimal import Decimal

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from shop.models import Product, Payment, OrderItem, Order


class TestDataBase(TestCase):
    fixtures = [
        "shop/fixtures/data.json"
    ]

    def setUp(self):
        self.user = User.objects.get(username='root')
        self.p = Product.objects.all().first()


    def test_user_exists(self):
                users = User.objects.all()
                users_number = users.count()
                user = users.first()
                self.assertEqual(users_number, 1)
                self.assertEqual(user.username, 'root')
                self.assertTrue(user.is_superuser)

    def test_user_check_password(self):
                self.assertTrue(self.user.check_password('123'))


    def test_all_date(self):
        self.assertGreater(Product.objects.all().count(),0)
        self.assertGreater(Order.objects.all().count(), 0)
        self.assertGreater(OrderItem.objects.all().count(), 0)
        self.assertGreater(Payment.objects.all().count(), 0)

    def find_cart_number(self):
        cart_number = Order.objects.filter(user=self.user,
                                           status=Order.STATUS_CART
                                           ).count()
        return cart_number

    def test_function_get_cart(self):
        """Check cart number
        1. No carts
        2. Create cart
        3. Get created cart
        =====================================
        Add @staticmethod Order.ger_cart(user)
        """
        pass
        # 1. No carts
        self.assertEqual(self.find_cart_number(), 0)

        # 2. Create cart
        Order.get_cart(self.user)
        self.assertEqual(self.find_cart_number(), 1)

        # 3. Get created cart
        Order.get_cart(self.user)
        self.assertEqual(self.find_cart_number(), 1)

    def test_cart_older_7_days(self):
        """If cart older than 7 days it must be deleted
        1. get cart and make it older
        =====================================
        Add some code to @staticmethod Order.ger_cart(user)
        """
        cart = Order.get_cart(self.user)
        cart.creation_time = timezone.datetime(2000, 1, 1, tzinfo=zoneinfo.ZoneInfo('UTC'))
        cart.save()
        cart = Order.get_cart(self.user)
        self.assertEqual((timezone.now() - cart.creation_time).days, 0)

    def test_recalculate_order_amount_after_changing_orderitem(self):
        """Checking cart amount
        1. Get order amount before any changing
        2. -------""------- after adding item
        3. -------""------- after deleting an item
        ==========================================
        Add amount to OrderItem as @property
        Add Order.get_amount(user)
        """
        # 1. Get order amount before any changing
        cart = Order.get_cart(self.user)
        self.assertEqual(cart.amount, Decimal(0))

        # 2. -------""------- after adding item
        i = OrderItem.objects.create(order=cart, product=self.p, price=2, quantity=2)
        i = OrderItem.objects.create(order=cart, product=self.p, price=2, quantity=3)
        cart = Order.get_cart(self.user)
        self.assertEqual(cart.amount, Decimal(10))
  #      #
        # # 3. -------""------- after deleting an item
        i.delete()
        cart = Order.get_cart(self.user)
        self.assertEqual(cart.amount, Decimal(4))
#
    def test_cart_status_changing_after_applying_make_order(self):
       """Check cart status change after Order.make_order()
       1. Attempt to change the status for an empty cart
       2. Attempt to change the status for a non-empty cart
       =======================================
       Add Order.make_order()
       """
       # 1. Attempt to change the status for an empty cart
       cart = Order.get_cart(self.user)
       cart.make_order()
       self.assertEqual(cart.status, Order.STATUS_CART)
#
       # 2. Attempt to change the status for a non-empty cart
       OrderItem.objects.create(order=cart, product=self.p, price=2, quantity=2)
       cart.make_order()
       self.assertEqual(cart.status, Order.STATUS_WAITING_FOR_PAYMENT)
#
    def test_method_get_amount_of_unpaid_orders(self):
  #      """Check @staticmethod get_amount_of_unpaid_orders() for several cases:
  #      1. Before creating cart
  #      2. After creating cart
  #      3. After cart.make_order()
  #      4. After order is paid
  #      5. After delete all orders
  #      ==================================
  #      Add Order.get_amount_of_unpaid_orders()
  #      """
  #      # 1. Before creating cart
        amount = Order.get_amount_of_unpaid_orders(self.user)
        self.assertEqual(amount, Decimal(13556))
#
        # 2. After creating cart
        cart = Order.get_cart(self.user)
        OrderItem.objects.create(order=cart, product=self.p, price=2, quantity=2)
        amount = Order.get_amount_of_unpaid_orders(self.user)
        self.assertEqual(amount, Decimal(13556))

        # 3. After cart.make_order()
        cart.make_order()
        amount = Order.get_amount_of_unpaid_orders(self.user)
        self.assertEqual(amount, Decimal(13560))

        # 4. After order is paid
        cart.status = Order.STATUS_PAID
        cart.save()
        amount = Order.get_amount_of_unpaid_orders(self.user)
        self.assertEqual(amount, Decimal(13556))

    # 5. After delete all orders


        Order.objects.all().delete()
        amount = Order.get_amount_of_unpaid_orders(self.user)
        self.assertEqual(amount, Decimal(0))


    def test_method_get_balance(self):
       """Check @staticmethod get_balance for several cases:
       1. Before adding payment
       2. After adding payment
       3. After adding some payments
       4. No payments
       ==================================
       Add Payment.get_balance()
       """
       #  1. Before adding payment
       amount = Payment.get_balance(self.user)
       self.assertEqual(amount, Decimal(13000))
#
       # 2. After adding payment
       Payment.objects.create(user=self.user, amount=100)
       amount = Payment.get_balance(self.user)
       self.assertEqual(amount, Decimal(13100))
#
       # 3. After adding some payments
       Payment.objects.create(user=self.user, amount=-50)
       amount = Payment.get_balance(self.user)
       self.assertEqual(amount, Decimal(13050))
#
       # 4. No payments
       Payment.objects.all().delete()
       amount = Payment.get_balance(self.user)
       self.assertEqual(amount, Decimal(0))



    def test_auto_payment_after_apply_make_order_true(self):
        """Check auto payment after applying make_order()
        1. There is a required amount
        """
        Order.objects.all().delete()
        cart = Order.get_cart(self.user)
        OrderItem.objects.create(order=cart, product=self.p, price=2, quantity=2)
        self.assertEqual(Payment.get_balance(self.user), Decimal(13000))
        cart.make_order()
        self.assertEqual(Payment.get_balance(self.user), Decimal(12996))

    def test_auto_payment_after_apply_make_order_false(self):
        """Check auto payment after applying make_order()
        2. There isn't a required amount
        """
        Order.objects.all().delete()
        cart = Order.get_cart(self.user)
        OrderItem.objects.create(order=cart, product=self.p, price=2, quantity=50000)
        cart.make_order()
        self.assertEqual(Payment.get_balance(self.user), Decimal(13000))

  #      # ==================== test tasks #8 =============================
#
    def test_auto_payment_after_add_required_payment(self):
        """There is unpaid order=13556 and balance=13000
        After applying payment=556:
            - order must change status
            - and balance must be 0
        """
        Payment.objects.create(user=self.user, amount=556)
        self.assertEqual(Payment.get_balance(self.user), Decimal(0))
        amount = Order.get_amount_of_unpaid_orders(self.user)
        self.assertEqual(amount, Decimal(0))

    def test_auto_payment_for_earlier_order(self):
        """There is unpaid order=13556 and balance=13000
        After creating new order=1000 applying payment=1000:
            - only earlier order must change status
            - and balance must be 13000+1000-13556
        """
        cart = Order.get_cart(self.user)
        OrderItem.objects.create(order=cart, product=self.p, price=2, quantity=500)
        cart.make_order()
        Payment.objects.create(user=self.user, amount=1000)
        self.assertEqual(Payment.get_balance(self.user), Decimal(444))
        amount = Order.get_amount_of_unpaid_orders(self.user)
        self.assertEqual(amount, Decimal(1000))

    def test_auto_payment_for_all_orders(self):
        """There is unpaid order=13556 and balance=13000
        After creating new order=1000 applying payment=10000:
            - all orders must be paid
        """
        cart = Order.get_cart(self.user)
        OrderItem.objects.create(order=cart, product=self.p, price=2, quantity=500)
        Payment.objects.create(user=self.user, amount=10000)
        self.assertEqual(Payment.get_balance(self.user), Decimal(9444))
        amount = Order.get_amount_of_unpaid_orders(self.user)
        self.assertEqual(amount, Decimal(0))