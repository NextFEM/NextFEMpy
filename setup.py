from setuptools import setup, find_packages

setup(
    name='nextfempy',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
            "requests"
    ],
    author='NextFEM',
    author_email='info@nextfem.it',
    description='NextFEM REST API wrapper in pure Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NextFEM/NextFEMpy',
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)