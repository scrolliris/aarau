from datetime import datetime
from peewee import (
    CharField,
    DateTimeField,
    FloatField,
    IntegerField,
    PrimaryKeyField,
    fn,
)

from aarau.models.base import AnalysisBase, NumericRangeField


class ReadingResult(AnalysisBase):
    id = PrimaryKeyField()
    element_id = CharField(max_length=255, unique=True)
    project_id = CharField(max_length=128)
    site_id = IntegerField()
    code = CharField(max_length=128)
    host = CharField(max_length=64)
    path = CharField(max_length=255)
    subject_type = CharField(max_length=16)
    subject_index = IntegerField()
    last_value = FloatField()
    mean_value = FloatField()
    sd_value = FloatField()
    median_value = FloatField()
    variance_value = FloatField()
    total_count = IntegerField()
    trusted_section = NumericRangeField()

    created_at = DateTimeField(null=False, default=datetime.utcnow)
    updated_at = DateTimeField(null=False, default=datetime.utcnow)

    class Meta:
        table_name = 'reading_results'

    def __repr__(self):
        return '<ReadingResult id:{} element_id:{} code:{} path:{}>'.format(
            self.id, self.element_id, self.code, self.path)

    def __json__(self, _req):
        return {'project_id': self.project_id,
                'site_id': self.site_id, 'path': self.path,
                'code': self.code,
                'paragraph_numbers': self.paragraph_numbers,
                'total_count': self.total_count}

    @classmethod
    def fetch_data_by_path(cls, project_access_key_id='', site_id=0):
        """Fetches result values by path."""
        return cls.select(
            cls.project_id,
            cls.site_id,
            cls.path,
            fn.Count(cls.subject_type).alias('paragraph_numbers'),
            fn.Sum(cls.total_count).alias('total_count')
        ).where(
            # not database id
            cls.project_id == project_access_key_id,
            cls.site_id == site_id,
            cls.subject_type == 'paragraph',
        ).group_by(
            cls.project_id,
            cls.site_id,
            cls.path,
        ).order_by(
            cls.path.asc(),
        )
