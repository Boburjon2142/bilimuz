from django.db import models
from backend.apps.catalog.models import Book


class Order(models.Model):
    PAYMENT_CHOICES = [
        ("cash", "Naqd"),
        ("bank", "Bank o‘tkazmasi"),
    ]
    STATUS_CHOICES = [
        ("new", "Yangi"),
        ("accepted", "Qabul qilindi"),
        ("delivering", "Yetkazilmoqda"),
        ("finished", "Yakunlangan"),
    ]

    full_name = models.CharField("F.I.Sh", max_length=255)
    phone = models.CharField("Telefon", max_length=50)
    extra_phone = models.CharField("Qo‘shimcha telefon", max_length=50, blank=True)
    address = models.CharField("Manzil", max_length=255)
    note = models.TextField("Izoh", blank=True)
    payment_type = models.CharField("To‘lov turi", max_length=20, choices=PAYMENT_CHOICES, default="cash")
    status = models.CharField("Holat", max_length=20, choices=STATUS_CHOICES, default="new")
    total_price = models.DecimalField("Umumiy summa", max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def line_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.book.title} x{self.quantity}"
