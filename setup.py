from setuptools import setup

setup(
    name="celebrity",
    version="0.1.0",
    packages=["celebrity"],
    package_dir={"celebrity": "celebrity"},
    description="Celebrity plugin",
    entry_points={
        "saleor.plugins": ["celebrity = celebrity.plugin:CelebrityPlugin"],
    },
)
