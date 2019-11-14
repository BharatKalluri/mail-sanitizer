from setuptools import setup

setup(
    name='mail-sanitizer',
    version='0.0.3',
    license="GPLv3",
    description="A cli tool to clean up your email",
    url="https://github.com/BharatKalluri/mail-sanitizer",
    packages=['mail_sanitizer'],
    install_requires=["PyYAML", "aiohttp", "pandas", "requests", "numpy", "google-auth", "click",
                      "google-auth-oauthlib"],
    entry_points={
        'console_scripts': [
            'mail-sanitizer = mail_sanitizer.main:main'
        ]
    },
    python_requires=">= 3.7",
    author="Bharat Kalluri",
    author_email="bharatkalluri@protonmail.com",
)
