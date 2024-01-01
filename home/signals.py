# signals.py
# signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Cars, Stock


# @receiver(post_save, sender=Cars)
# def update_stock(sender, instance, created, **kwargs):
#     if created:
#         stock, stock_created = Stock.objects.get_or_create(variant=instance)
#         if not stock_created:
#             stock.stock += 1
#             stock.save()
