"""
SunPy: Python for Solar Physics

The SunPy project is an effort to create an open-source software library for
solar physics using the Python programming language.
"""
import platform

DOCLINES = __doc__.split("\n")

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Physics',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Operating System :: MacOS'
]

VERSION = '0.5.3'

def git_description():
    import subprocess
    try:
        out = subprocess.Popen(['git', 'describe', '--tags'], stdout = subprocess.PIPE).communicate()[0]
        description = out.strip().decode('ascii')
    except OSError:
        description = 'Error: could not run git'
    return description

def write_version_py():
    import os
    if os.path.exists('.git'):
        GIT_DESCRIPTION = git_description()
    else:
        GIT_DESCRIPTION = 'N/A'

    out = open('sunpy/version.py', 'w')
    template = """# This file is automatically generated by SunPy's setup.py
version = '%(version)s'
git_description = '%(git_description)s'
"""
    try:
        out.write(template % {'version': VERSION,
                              'git_description': GIT_DESCRIPTION})
    finally:
        out.close()


def install(setup): #pylint: disable=W0621
    from setuptools import find_packages
    #Crotate Module
    from distutils.core import Extension
    from os.path import dirname, join

    try:
        import numpy as np
    except ImportError:
        print("SunPy WARNING: NumPy must be installed first to build the C extension")

    if 'np' in locals():
        libs = ['m']
        gcc_args = ['-std=c99', '-O3']

        module_ana = 'sunpy.io._pyana'
        sourcefiles_ana = [join('.', 'sunpy', 'io', 'src', 'ana', 'anacompress.c'),
                           join('.', 'sunpy', 'io', 'src', 'ana', 'anadecompress.c'),
                           join('.', 'sunpy', 'io', 'src', 'ana', 'anarw.c'),
                           join('.', 'sunpy', 'io', 'src', 'ana', 'testrw.c'),
                           join('.', 'sunpy', 'io', 'src', 'ana', '_pyana.c')]

        ana = Extension(module_ana,
                            sources = sourcefiles_ana,
                            libraries = libs,
                            extra_compile_args = gcc_args,
                            include_dirs =
                            [np.get_include(), join('.', 'sunpy', 'io', 'src')]
                            )
    ext_modules = []
    if 'ana' in locals() and platform.system() != 'Windows' :
        ext_modules.append(ana)

    write_version_py()

    # Define the extra requirements in a sensible manner.
    extras_require = {'database': ["sqlalchemy"],
                      'image': ["scikit-image"],
                      'jpeg2000': ["glymur"],
                      'net': ["suds", "beautifulsoup4", "requests"]}
    # All is everything except glymur.
    extras_require['all'] = extras_require['database'] + extras_require['image'] + extras_require['net']

    setup(
	author="Steven Christe, Russell Hewett, Keith Hughitt, Jack Ireland, Florian Mayer, Stuart Mumford,  Albert Shih, David Perez-Suarez et. al",
        author_email="sunpy@googlegroups.com",
        classifiers=CLASSIFIERS,
        description=DOCLINES[0],
        install_requires=[
            'numpy>1.7.1',
            'astropy>=0.3.1',
            'scipy',
            'pandas>=0.12.1',
            'matplotlib>=1.1',
        ],
        extras_require=extras_require,
        license="BSD",
        long_description="\n".join(DOCLINES[2:]),
        maintainer="SunPy Developers",
        maintainer_email="sunpy@googlegroups.com",
        name="sunpy",
        packages=find_packages(),
        package_data={'': ['*.fits', '*.fit', 'sunpyrc']},
        platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
        provides=['sunpy'],
        url="http://www.sunpy.org/",
        use_2to3=True,
        include_package_data=True,
        zip_safe=False,
        version=VERSION,
        ext_modules = ext_modules
    )

if __name__ == '__main__':
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
    install(setup)
