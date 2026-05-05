from setuptools import setup, find_packages

setup(
    name="sentcluster",
    version="0.1.0",
    description="A tool for sentence clustering.",
    packages=find_packages(),
    install_requires=[
        "scikit_learn~=1.7.1",
        "sentence_transformers~=5.1.0"
    ],
    python_requires=">=3.7",
    include_package_data=True,
)
