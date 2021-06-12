from setuptools import setup


with open("README.md", "r") as desc:
    long_description = desc.read()


setup(
	name="xtractmime",
	version="1.0.0",
	description="Package for sniffing MIME(Multipurpose Internet Mail Extension) types",
	long_description=long_description,
	long_description_content_type="text/markdown",
	author="Akshay Sharma",
	author_email="akshaysharmajs@gmail.com",
	url="https://github.com/scrapy/xtractmime.git",
	packages=["xtractmime"],
	python_requires="",
	classifiers=[
					
				]

)