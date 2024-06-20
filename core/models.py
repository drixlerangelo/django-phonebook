from django.db import models
from django.db.models.signals import pre_delete, post_delete


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    def delete(self):
        # Manually send pre_delete signal
        pre_delete.send(sender=self.__class__, instance=self)

        # Update is_deleted directly in the database
        # Avoids sending the post_save signal
        type(self).objects.filter(pk=self.pk).update(is_deleted=True)

        # Manually send post_delete signal
        post_delete.send(sender=self.__class__, instance=self)

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True
