from setuptools import find_packages, setup

with open("requirements.txt", encoding="UTF8") as f:
    requirements = f.read().splitlines()

setup(
    name="morse-pi",
    version="0.1",
    description="Morse Pi (Raspberry Pi Morse Device)",
    packages=find_packages(where=".", exclude=("tests", "tests.*", "data", "data.*")),
    package_dir={"morse_pi": "morse_pi"},
    install_requires=requirements,
)
