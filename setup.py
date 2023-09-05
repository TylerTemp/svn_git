import sys
from setuptools import setup

setup(
    name='snv_git',
    version='0.0.2',
    author='TylerTemp',
    author_email='tylertempdev@gmail.com',
    description='svn commit to git commit',
    license='MIT',
    keywords='svn git version control',
    # url='',
    py_modules=['svn_git'],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        # 'GitPython',
        'pysvn',
        'pytz',
        'tzlocal',
        'docpie',
    ],
    tests_require=[],
    cmdclass={},
    entry_points={
        'console_scripts': [
            'svn_git = svn_git:main'
        ]
    },
)
