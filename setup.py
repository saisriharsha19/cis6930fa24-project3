from setuptools import setup, find_packages

setup(
	name='project0',
	version='1.0',
	author='Sai Sri Harsha Guddati',
	author_email='saisriha.guddati@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs', 'resources')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)