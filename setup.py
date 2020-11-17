from setuptools import setup

setup(
    name='NlpToolkit-MorphologicalDisambiguation',
    version='1.0.8',
    packages=['MorphologicalDisambiguation'],
    url='https://github.com/olcaytaner/TurkishMorphologicalDisambiguation-Py',
    license='',
    author='olcay',
    author_email='olcaytaner@isikun.edu.tr',
    description='Turkish Morphological Disambiguation Library',
    install_requires=['NlpToolkit-MorphologicalAnalysis', 'NlpToolkit-NGram']
)
