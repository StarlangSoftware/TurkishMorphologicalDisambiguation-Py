from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='NlpToolkit-MorphologicalDisambiguation',
    version='1.0.15',
    packages=['MorphologicalDisambiguation', 'MorphologicalDisambiguation.data'],
    package_data={'MorphologicalDisambiguation.data': ['*.txt']},
    url='https://github.com/StarlangSoftware/TurkishMorphologicalDisambiguation-Py',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Turkish Morphological Disambiguation Library',
    install_requires=['NlpToolkit-MorphologicalAnalysis', 'NlpToolkit-NGram'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
