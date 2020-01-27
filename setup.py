from setuptools import setup

setup(
    name='NlpToolkit-MorphologicalDisambiguation',
    version='1.0.0',
    packages=['MorphologicalDisambiguation'],
    url='https://github.com/olcaytaner/TurkishMorphologicalDisambiguation-Py',
    license='',
    author='olcay',
    author_email='olcaytaner@isikun.edu.tr',
    description='Turkish Morphological Disambiguation Library',
    requires=['NlpToolkit-MorphologicalAnalysis', 'NlpToolkit-NGram']
)
