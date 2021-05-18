from setuptools import setup

setup(
    name='NlpToolkit-MorphologicalDisambiguation',
    version='1.0.12',
    packages=['MorphologicalDisambiguation'],
    url='https://github.com/StarlangSoftware/TurkishMorphologicalDisambiguation-Py',
    license='',
    author='olcay',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Turkish Morphological Disambiguation Library',
    install_requires=['NlpToolkit-MorphologicalAnalysis', 'NlpToolkit-NGram']
)
