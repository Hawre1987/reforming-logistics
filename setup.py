from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in oil_gas_logistics/__init__.py
import re
with open("oil_gas_logistics/__init__.py") as f:
	version = re.search(r'__version__\s*=\s*[\'"]([^\'"]+)[\'"]', f.read()).group(1)

setup(
	name="oil_gas_logistics",
	version=version,
	description="Managing Logistics for Oil & Gas ",
	author="botan.b.abdullah@gmail.com",
	author_email="botan.b.abdullah@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
