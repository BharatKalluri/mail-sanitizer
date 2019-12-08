from setuptools import setup, find_packages

setup(
    name='mail-sanitizer',
    version='0.0.7',
    license="GPLv3",
    description="A cli tool to clean up your email",
    url="https://github.com/BharatKalluri/mail-sanitizer",
    packages=find_packages(),
    install_requires=["PyYAML", "aiohttp", "pandas", "requests", "numpy", "google-auth", "click",
                      "google-auth-oauthlib", "halo"],
    entry_points={
        'console_scripts': [
            'mail-sanitizer = mail_sanitizer.main:main'
        ]
    },
    python_requires=">= 3.5",
    author="Bharat Kalluri",
    author_email="bharatkalluri@protonmail.com",
)
