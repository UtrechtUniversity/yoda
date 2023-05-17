from setuptools import setup

DOC = \
      """
      DMF Mockup dmattr dmget dmls dmput
      """

setup(
    name='dm-mock',
    version='0.8.3',
    long_description=DOC,
    packages=['dm_mock', 'dm_server', 'dm_server'],
    include_package_data=False,
    zip_safe=False,
    install_requires=['Flask==2.0.3',
                      'requests==2.27.1',
                      'numpy==1.19.5',
                      'typing-extensions==4.1.1',
                      'Werkzeug==2.0.3'],
    entry_points='''
    [console_scripts]
    dmattr=dm_mock:dmattr
    dmget=dm_mock:dmget
    dmls=dm_mock:dmls
    dmput=dm_mock:dmput
    dm_server=dm_server.app:run_app
    ''')
