import setuptools


setuptools.setup(
    name="django-jsonstore",
    version="26.7.0",
    author="Mikhail Podgurskiy",
    author_email="kmmbvnr@gmail.com",
    description="Expose JSONField data as virtual django model fields.",
    long_description=open("README.rst", "r", encoding="utf-8").read(),
    long_description_content_type="text/x-rst",
    license="AGPL-3.0-or-later WITH viewflow-library-exception",
    license_files=["LICENSE", "LICENSE_EXCEPTION"],
    platforms=["Any"],
    keywords=["django", "json", "orm", "jsonfield", "schemaless"],
    url="https://github.com/viewflow/jsonstore",
    project_urls={
        "Source": "https://github.com/viewflow/jsonstore",
        "Changelog": "https://github.com/viewflow/jsonstore/blob/master/CHANGELOG.rst",
        "Issues": "https://github.com/viewflow/jsonstore/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Django :: 5.2",
        "Framework :: Django :: 6.0",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    ],
    install_requires=[
        # Only Django versions still under upstream support.
        "Django>=5.2",
    ],
    packages=setuptools.find_packages(include=["jsonstore*"]),
    include_package_data=True,
    python_requires=">=3.10",
    zip_safe=False,
)
