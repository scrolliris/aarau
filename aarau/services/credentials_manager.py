import redis


class CredentialsManager():
    """Service object to manage site credentials."""

    def __init__(self, *args, **_kwargs):
        req = args[0]
        pool = redis.ConnectionPool.from_url(req.settings['store.url'])
        self.client = redis.Redis(connection_pool=pool)
        self.site = None

        super().__init__()  # takes no arguments

    def assign(self, obj=None):
        """Assigns a site."""
        if obj:
            self.site = obj

    def sync(self):
        """Creates or updates site credentials."""
        # TODO: raises appropriate exception
        if not self.site:
            raise Exception()

        project = self.site.project
        name = '{}-{}'.format(project.id, self.site.id)

        # name: project.id-site.id
        return self.client.hmset(name, {
            'project_access_key_id': project.access_key_id,
            'site_id': self.site.id,
            'read_key': self.site.read_key,
            'write_key': self.site.write_key,
        })

    def validate(self) -> bool:
        """Checks credentials stored in db are valid."""
        if not self.site:
            return False

        project = self.site.project
        name = '{}-{}'.format(project.id, self.site.id)

        expected = {
            'project_access_key_id': project.access_key_id,
            'site_id': self.site.id,
            'read_key': self.site.read_key,
            'write_key': self.site.write_key,
        }
        values = {k: self.client.hget(name, k) for k in expected}
        result_set = list({
            v is not None and str(expected[k]) == v.decode()
            for k, v in values.items()
        })
        return [True] == result_set

    def destroy(self) -> bool:  # pylint: disable=no-self-use
        # TODO
        return False
