from setuptools import setup

setup(
    name='resif',
    version='0.1',
    py_modules=['resif', 'configManager', 'bootstrapEB', 'buildSwSets'],
    install_requires=[
        'click',
        'GitPython',
    ],
    entry_points='''
        [console_scripts]
        resif=resif:resif
    ''',
)
