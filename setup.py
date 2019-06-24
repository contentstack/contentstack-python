from setuptools import setup
package = 'contentstack'
requirements = [
    'requests>=2.20.0,<3.0',
    'python-dateutil'
]
setup(
    name='contentstack-python',
    version='1.0.0',
    packages=['contentstack', 'doc', 'tests'],
    url='https://www.contentstack.com',
    license='MIT License',
    author='Shailesh Mishra',
    author_email='shailesh.mishra@contentstack.com',
    description='Create python-based applications and use the python SDK to fetch and deliver content from Contentstack. The SDK uses Content Delivery APIs. ',
    install_requires=['requests', 'config']
)

