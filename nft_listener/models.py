from django.db import models

class TransferEvent(models.Model):
    token_id = models.CharField(max_length=255)
    from_address = models.CharField(max_length=255)
    to_address = models.CharField(max_length=255)
    transaction_hash = models.CharField(max_length=255)
    block_number = models.IntegerField()