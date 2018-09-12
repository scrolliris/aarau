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

        site = self.site
        project = site.project

        for ctx in ('read', 'write'):
            # project.access_key_id-read: {...}
            name = '{}-{}'.format(project.access_key_id, ctx)
            values = self.client.hgetall(name)

            # {read_key: site_id, ...}
            for k, v in values.items():
                if v.decode() == site.id:
                    values.pop(k, None)

            key = site.__dict__['__data__']['{}_key'.format(ctx)]
            values[key] = site.id
            self.client.hmset(name, values)

        return True

    def validate(self, ctx) -> bool:
        """Checks credentials stored in db are valid."""
        if not self.site:
            return False

        site = self.site
        project = site.project

        name = '{}-{}'.format(project.access_key_id, ctx)

        key = site.__dict__['__data__']['{}_key'.format(ctx)]

        site_id = self.client.hget(name, key)
        return site_id is not None and str(site.id) == site_id.decode()

    def destroy(self) -> bool:  # pylint: disable=no-self-use
        # TODO
        return False
