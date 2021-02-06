"""
Script used for package configuration and installation
"""

from setuptools import find_packages, setup


with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name='cdslab_auth',
    version='0.0.1',
    maintainer='Developers of the CDS team of FEnFiSDi group',
    maintainer_email='alejandro.campillo@udea.edu.co',
    description='Authentication API for CDSLab',
    long_description=long_description,
    url='https://github.com/fenfisdi/cdslab_auth',
    author='Alejandro Campillo',
    author_email='alejandro.campillo@udea.edu.co',
    license='GNU General Public License v3 (GPLv3)',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Framework :: CDSLab',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries'
        ],
    test_suite='pytest',
    packages=find_packages(exclude='__pycache__'),
    keywords=[
        'Computation',
        'Authentication',
        'Security',
        '2FA'
        ],
    python_requires='>=3.5',
    install_requires=[],
    zip_safe=False
    )