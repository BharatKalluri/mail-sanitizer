from setuptools import setup

setup(
    name='mail-sanitizer',
    version='0.0.2',
    packages=['cli'],
    install_requires=["PyYAML", "aiohttp", "pandas", "requests", "numpy", "google-auth", "click",
                      "google-auth-oauthlib"],
    entry_points={
        'console_scripts': [
            'mail-sanitizer = cli.main:main'
        ]
    },
)
