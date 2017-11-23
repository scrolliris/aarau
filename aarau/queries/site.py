from aarau.models import (  # noqa  # pylint: disable=unused-import
    Site,
    Project,
    Application,
    Publication,
    License,
    Classification,
)


def get_sites(site_type, limit=10):
    site_class = globals()[site_type.capitalize()]

    sites = Site.select().join(
        site_class,
        on=(Site.hosting_id == site_class.id).alias(site_type)
    ).switch(Site).join(
        Project
    )
    if site_type == 'application':
        sites = sites.select(
            Site, Project, site_class
        )
    else:
        sites = sites.select(
            Site, Project, site_class, License, Classification
        ).switch(Publication).join(
            License,
            on=(Publication.license_id == License.id)
        ).switch(Publication).join(
            Classification,
            on=(Publication.classification_id == Classification.id)
        )

    sites = sites.where(
        Site.hosting_type == site_type.capitalize()
    ).limit(limit)

    return sites
