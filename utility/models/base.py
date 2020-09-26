from django.db import models


class BaseModel(models.Model):
    """
    A table for storing generic timestamp information about an object
    """
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class BaseAuditModel(BaseModel):
    """
    A table for storing generic user change information about an object
    """
    created_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='created_by', related_name='%(class)s_created_by')
    last_modified_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='last_modified_by', related_name='%(class)s_last_modified', blank=True, null=True)
    deleted_by = models.ForeignKey('identity.Identity', models.DO_NOTHING, db_column='deleted_by', related_name='%(class)s_deleted_by', blank=True, null=True)

    class Meta:
        abstract = True
