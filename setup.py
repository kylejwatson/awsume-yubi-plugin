from setuptools import setup

setup(
    name='awsume-yubi-plugin',
    version='0.0.0',
    entry_points={
        'awsume': [
            'yubi = yubi'
        ]
    },
    author='Kyle Watson',
    author_email='kyle.watson@woodwing.com',
    py_modules=['yubi'],
)
