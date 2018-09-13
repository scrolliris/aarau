# pylint: disable=invalid-name
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, *('doc', 'DESCRIPTION.rst'))) as f:
    DESCRIPTION = f.read()
with open(os.path.join(here, 'CHANGELOG')) as f:
    CHANGELOG = f.read()

requires = [
    'beaker',
    'bleach',
    'bcrypt',
    'celery[redis]',
    'itsdangerous',
    'MarkupSafe',
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
    'pyramid_secure_response',
    'pyramid_services',
    'PyYAML',
    'redis',
    'requests',
    'transaction',
    'webob',
    'WTForms',

    'wsgi-basic-auth',
]

development_requires = [
    'colorlog',
    'waitress',

    'pydocstyle',
    'pycodestyle',
    'pylint',
]

testing_requires = [
    'colorlog',
    'waitress',

    'mixer',
    'pytest',
    'pytest-cov',
    'pytest-mock',
    'pytest-selenium',
    'selenium',
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
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
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
    entry_points="""\
    [paste.app_factory]
    main = aarau:main
    [console_scripts]
    aarau_manage = aarau.scripts.manage:main
    aarau_pserve = aarau.scripts.pserve:main
    aarau_pshell = aarau.scripts.pshell:main
    aarau_pstart = aarau.scripts.pstart:main
    aarau_worker = aarau.scripts.worker:main
    """,
)
