from setuptools import setup

setup(
    name="Thermal simulation project",
    version="1.0.0",
    description="This project aims to provide a tool to perform versatile temperature simulation of known systems and to characterize unknown ones thermally.",
    author="Alessandro Galeazzi",
    author_email = "alessandro.galeazzi3@studio.unibo.it",
    url = "https://github.com/AlessandroGaleazzi/S-C_2022_galeazzi",
    packages=["functions"],
    install_requires=[
        "configparser",
        "matplotlib",
        "numpy",
        "scipy",
        "pandas",
        "pytest",
        "pytest-cov",
    ],
)