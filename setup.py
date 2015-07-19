#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os


from distutils import log
from setuptools import setup
from setuptools.command.install import install


kernel_json = {"argv":["python3","-m","mochikernel", "-f", "{connection_file}"],
 "display_name":"Mochi",
 "language":"python",
 "codemirror_mode":"python"
}


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

#stolen from bash kernel

class install_with_kernelspec(install):
    def run(self):
        # Regular installation
        install.run(self)

        # Now write the kernelspec
        from IPython.kernel.kernelspec import install_kernel_spec
        from IPython.utils.tempdir import TemporaryDirectory
        with TemporaryDirectory() as td:
            os.chmod(td, 0o755) # Starts off as 700, not user readable
            with open(os.path.join(td, 'kernel.json'), 'w') as f:
                json.dump(kernel_json, f, sort_keys=True)
            # TODO: Copy resources once they're specified

            log.info('Installing IPython kernel spec')
            install_kernel_spec(td, 'mochi', user=True, replace=True)


setup(
    name='mochikernel',
    version='0.2.0',
    description='Python Boilerplate contains all the boilerplate you need to create a Python package.',
    long_description=readme + '\n\n' + history,
    author='Matthias Bussonnier, Mike Müller',
    author_email='bussonniermatthias@gmail.com, pymmueller@gmail.com',
    url='https://github.com/Carreau/mochi-kernel',
    packages=[
        'mochikernel',
    ],
    package_dir={'mochikernel':
                 'mochikernel'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='mochikernel',
    cmdclass={'install': install_with_kernelspec},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
