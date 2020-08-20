import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
     name='sss_beneficiarios_hospitales',
     version='0.8.117',
     license='MIT',
     entry_points={
        },
     author="Andres Vazquez",
     author_email="andres@data99.com.ar",
     description="API Superintendencia de Servicios de Salud Argentino para informacion sobre beneficiarios de hospitales",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/cluster311/sss-beneficiarios",
     install_requires=required,
     # package_dir={'': 'src'},
     packages=['sss_beneficiarios_hospitales'],  # setuptools.find_packages(),
     package_data = {
        'html-samples': ['*']
        },
     classifiers=[
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.6',
         'Programming Language :: Python :: 3.7',
         'Programming Language :: Python :: 3.8',
         'License :: OSI Approved :: MIT License',
         'Operating System :: OS Independent',
         'Intended Audience :: Developers', 
     ],
     python_requires='>=3.6',
 )
