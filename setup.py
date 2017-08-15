# pylint: disable=C0103
"""Setup script.
"""

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, *('doc', 'DESCRIPTION.rst'))) as f:
    DESCRIPTION = f.read()
with open(os.path.join(here, 'CHANGELOG')) as f:
    CHANGELOG = f.read()

requires = [
    'beaker',
    'bcrypt',
    'celery[redis]',
    'colorlog',
    'google-cloud-datastore',
    'itsdangerous',
    'Paste',
    'PasteScript',
    'peewee',
    'peewee_migrate',
    'psycopg2',
    'pylibmc',
    'python-dotenv',
    'pyramid',
    'pyramid_assetviews',
    'pyramid_beaker',
    'pyramid_celery',
    'pyramid_mako',
    'pyramid_mailer',
    'pyramid_services',
    'requests',
    'transaction',
    'webob',
    'WTForms',

    'wsgi-basic-auth',
]

development_requires = [
    'flake8',
    'flake8_docstrings',
    'pylint',
    'PyYAML',
    'waitress',
]

testing_requires = [
    'mixer',
    'pytest',
    'pytest-cov',
    'pytest-mock',
    'PyYAML',
    'WebTest',
]

production_requires = [
    'CherryPy',
    'honcho',
]

setup(
    name='aarau',
    version='0.0.1',
    description='aarau',
    long_description=DESCRIPTION + '\n\n' + CHANGELOG,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web wsgi pylons pyramid',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'development': development_requires,
        'testing': testing_requires,
        'production': production_requires,
    },
    install_requires=requires,
    message_extractors={'aarau': [
        ('**.py', 'python', None),
        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
        ('static/**', 'ignore', None),
    ]},
    entry_points="""\
    [paste.app_factory]
    main = aarau:main
    [console_scripts]
    aarau_manage = aarau.scripts.manage:main
    aarau_pserve = aarau.scripts.pserve:main
    aarau_pstart = aarau.scripts.pstart:main
    aarau_worker = aarau.scripts.worker:main
    """,
)
