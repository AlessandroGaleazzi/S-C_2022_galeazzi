from setuptools import setup

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.readlines()
    requirements = [x[:-1] for x in requirements]

setup(
    name="Thermal simulation project",
    version="1.0.0",
    description="This project aims to provide a tool to perform versatile temperature simulation of known systems and to characterize unknown ones thermally.",
    author="Alessandro Galeazzi",
    author_email = "alessandro.galeazzi3@studio.unibo.it",
    url = "https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi",
    packages=["functions"],
    install_requires=requirements
)