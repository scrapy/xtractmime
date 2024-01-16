import setuptools


with open("README.md", "r", encoding="utf-8") as desc:
    long_description = desc.read()

setuptools.setup(
    name="xtractmime",
    version="0.2.1",
    license="BSD",
    description=(
        "Implementation of the MIME Sniffing standard  (https://mimesniff.spec.whatwg.org/)"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Akshay Sharma",
    author_email="akshaysharmajs@gmail.com",
    url="https://github.com/scrapy/xtractmime",
    packages=["xtractmime"],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Framework :: Scrapy",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
