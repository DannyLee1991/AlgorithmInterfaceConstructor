from setuptools import setup

setup(
    name='aic',
    version='0.2',
    author="Dannylee",
    author_email="747554505@qq.com",
    license="MIT",
    url="https://github.com/DannyLee1991/AlgorithmInterfaceConstructor",
    py_modules=['app'],
    install_requires=[
        'Click',
        'pyyaml',
        'python-grpc'
    ],
    entry_points='''
        [console_scripts]
        aic=app:aic
    ''',
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Multimedia :: Video',
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=True,
)
