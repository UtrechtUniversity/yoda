from setuptools import setup, find_packages

DOC = """
Data Archive mock server: daattr daget dals darelease
"""

setup(
    name='da-mock',
    version='0.9.0',
    long_description=DOC,
    long_description_content_type='text/plain',
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'Flask==3.1.1',
        'requests==2.32.4',
        'numpy==2.3.1',
        'typing-extensions==4.14.1',
        'urllib3==2.6.0',
        'Werkzeug==3.1.4'
    ],
    entry_points={
        'console_scripts': [
            'daattr=da_mock:daattr',
            'daget=da_mock:daget',
            'dals=da_mock:dals',
            'darelease=da_mock:darelease',
            'da_server=da_server.app:run_app',
        ],
    },
    python_requires='>=3.9',
)
