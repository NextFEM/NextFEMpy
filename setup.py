from setuptools import setup, find_packages

setup(
    name='NextFEMpy',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
            "requests",
            "json"
    ],
    author='NextFEM',
    author_email='info@nextfem.it',
    description='NextFEM REST API wrapper in pure Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NextFEM/NextFEMpy',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSS Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)