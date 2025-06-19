from setuptools import setup, find_packages

DOC = """
DMF Mockup dmattr dmget dmls dmput
"""

setup(
    name='dm-mock',
    version='0.8.5',
    long_description=DOC,
    long_description_content_type='text/plain',
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'Flask==3.0.2',
        'requests==2.32.4',
        'numpy==2.0.2',
        'typing-extensions==4.1.1',
        'urllib3>=1.21.1,<3',
        'Werkzeug==3.0.6'
    ],
    entry_points={
        'console_scripts': [
            'dmattr=dm_mock:dmattr',
            'dmget=dm_mock:dmget',
            'dmls=dm_mock:dmls',
            'dmput=dm_mock:dmput',
            'dm_server=dm_server.app:run_app',
        ],
    },
    python_requires='>=3.9',
)
