from setuptools import setup


with open("README.md", "r") as desc:
    long_description = desc.read()


setup(
	name="xtractmime",
	version="1.0.0",
	license="BSD",
	description="Implementation of the MIME Sniffing standard (https://mimesniff.spec.whatwg.org/)",
	long_description=long_description,
	long_description_content_type="text/markdown",
	author="Akshay Sharma",
	author_email="akshaysharmajs@gmail.com",
	url="https://github.com/scrapy/xtractmime.git",
	packages=["xtractmime"],
	python_requires=">=3.6",
	classifiers=[ 
				"Development Status :: 5 - Production/Stable",
				"Intended Audience :: Developers",
				"License :: OSI Approved :: BSD License",
				"Operating System :: OS Independent",
				"Programming Language :: Python :: 3 :: Only",
			    "Programming Language :: Python :: 3.6",
			    "Programming Language :: Python :: 3.7",
			    "Programming Language :: Python :: 3.8",
			    "Programming Language :: Python :: 3.9",
			    "Topic :: Internet",
			    "Topic :: Software Development :: Libraries :: Python Modules",
			],

)