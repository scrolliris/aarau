from playhouse.pool import PooledPostgresqlDatabase


class DB(dict):
    """Database connections."""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


db = DB({  # pylint: disable=invalid-name
    'cardinal': PooledPostgresqlDatabase(None, field_types={
        'e_user_activation_state': 'enum'
    }),
    'analysis': PooledPostgresqlDatabase(None, field_types={
        'e_user_activation_state': 'enum'})
})
