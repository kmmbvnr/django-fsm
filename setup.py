from pathlib import Path

import setuptools

ROOT = Path(__file__).resolve().parent

setuptools.setup(
    name="django-fsm",
    version="5.0.2",
    description="State machines for Python objects and Django models.",
    long_description=(ROOT / "README.rst").read_text(encoding="utf-8"),
    long_description_content_type="text/x-rst",
    author="Mikhail Podgurskiy",
    author_email="kmmbvnr@gmail.com",
    url="https://github.com/viewflow/django-fsm",
    license="AGPL-3.0-or-later WITH viewflow-library-exception",
    license_files=["LICENSE", "LICENSE_EXCEPTION", "LICENSE_LEGACY"],
    platforms=["Any"],
    keywords=["django", "fsm", "state-machine", "workflow"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
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
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.10",
    install_requires=[],
    extras_require={
        "django": ["Django>=5.2"],
        "graphviz": ["graphviz>=0.20"],
        "rest": ["Django>=5.2", "djangorestframework>=3.11", "drf-spectacular>=0.26.2"],
        "test": ["Django>=5.2", "django-guardian>=2.4", "graphviz>=0.20"],
        "typing": ["Django>=5.2", "mypy>=1.11", "pyright>=1.1.390", "django-stubs>=5.2"],
        "all": [
            "Django>=5.2",
            "django-guardian>=2.4",
            "graphviz>=0.20",
            "djangorestframework>=3.11",
            "drf-spectacular>=0.26.2",
        ],
    },
    packages=setuptools.find_packages(
        include=["django_fsm*"], exclude=["django_fsm.tests*"]
    ),
    include_package_data=False,
    package_data={"django_fsm": ["py.typed"]},
    zip_safe=False,
)
