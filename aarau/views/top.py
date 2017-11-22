from pyramid.view import view_config

from aarau.models import (  # noqa  # pylint: disable=unused-import
    Site,
    Application,
    Publication,
    License,
    Classification,
)
from aarau.views import tpl


def get_site_type(params):
    site_type = 'publication' if (
        'type' not in params or params['type'] == 'publication'
    ) else 'application'
    return site_type


def get_site_objects(site_type, limit=10):
    site_class = globals()[site_type.capitalize()]

    sites = Site.by_type(site_type).order_by(Site.id.desc()).limit(limit)
    object_ids = [s.hosting_id for s in sites]

    if site_type == 'application':
        site_objects = site_class.select(site_class)
    else:
        site_objects = site_class.select(
            site_class, Classification, License
        ).join(
            Classification, on=(
                site_class.classification_id == Classification.id)
        ).switch(site_class).join(
            License, on=(site_class.license_id == License.id)
        )

    return site_objects.where(
        site_class.id << object_ids
    ).order_by(
        site_class.id.desc()
    )


@view_config(route_name='top', renderer=tpl('top.mako'))
def top(req):
    site_type = get_site_type(req.params)
    site_objects = get_site_objects(site_type)

    return dict(site_type=site_type, site_objects=site_objects)
