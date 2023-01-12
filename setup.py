from setuptools import find_packages, setup

setup(
    name='sdk-remote-controller',
    packages=find_packages(),
    version='0.1.0',
    description='Library for executing android sdk methods throw the shell',
    author='Dmytro Frolov',
    license='MIT',
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.xml', '*.special', '*.apk'],
    },
    install_requires=['setuptools', 'importlib-resources', 'loguru'],
    setup_requires=['setuptools', 'importlib-resources', 'loguru'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)
