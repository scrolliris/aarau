"""Site replication service.
"""
from google.cloud import datastore


class SiteReplicator(object):
    """Service object for site replication.
    """

    def __init__(self, *_args, **_kwargs):
        self.client = datastore.Client()
        self.site = None

        super().__init__()  # takes no arguments

    def assign(self, obj=None):
        """Assigns appropriate object; site.
        """
        if obj:
            self.site = obj

    def replicate(self):
        """Creates or updates appropriate site object.
        """
        # FIXME: raises valid exception
        if not self.site:
            raise Exception()

        project = self.site.project

        # project.id + site.id
        with self.client.transaction():
            site_key = self.client.key(
                'Site', '{}-{}'.format(project.id, self.site.id))
            obj = datastore.Entity(key=site_key)
            obj.update({
                'project_access_key_id': project.access_key_id,
                'site_id': self.site.id,
                'read_key': self.site.read_key,
                'write_key': self.site.write_key,
            })
            return self.client.put(obj)

    def validate(self):
        """Checks entity in datastore.
        """
        if not self.site:
            return False

        project = self.site.project

        query = self.client.query(kind='Site')
        query.add_filter('project_access_key_id', '=', project.access_key_id)
        query.add_filter('read_key', '=', self.site.read_key)
        query.add_filter('write_key', '=', self.site.write_key)
        query.keys_only()

        sites = list(query.fetch() or ())
        if len(sites) != 1:
            return False

        site_key = self.client.key(
            'Site', '{}-{}'.format(project.id, self.site.id))
        _obj = sites[0]
        return _obj.key == site_key
