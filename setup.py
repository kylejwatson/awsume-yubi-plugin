from setuptools import setup, find_packages

setup(
    name='awsume-yubi-plugin',
    packages=find_packages(),
    version='0.2.1',
    entry_points={
        'awsume': [
            'yubi = yubi'
        ]
    },
    author='Kyle Watson',
    author_email='kyle.watson@woodwing.com',
    py_modules=['yubi'],
    description='Plugin to use a Yubikey with awsume',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/kylejwatson/awsume-yubi-plugin',
    install_requires=[
        'awsume~=4.5.4',
        'yubikey-manager~=5.3.0',
    ]
)
