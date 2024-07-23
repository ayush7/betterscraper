import setuptools
from pathlib import Path

# Read requirements.txt and parse it
def parse_requirements(filename):
    requirements = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                package = line.split('==')[0]
                requirements[package] = line
    return requirements

requirements = parse_requirements('requirements.txt')

print("Requirements:", requirements)

# Define all requirements
all_requirements = list(requirements.values())

# Define base requirements
# base_requirements = [
#     requirements['stream2sentence'],
#     requirements['pydub'],
#     requirements['pyaudio']
# ]

# Define subsets of requirements for each engine
# extras_require = {
#     # 'minimal': base_requirements,
#     # 'all': base_requirements + [requirements['pyttsx3']] + [requirements['azure-cognitiveservices-speech']] + [requirements['elevenlabs']] + [requirements['openai']] + [requirements['gtts']] + [requirements['coqui_tts']],
#     # 'system': base_requirements + [requirements['pyttsx3']],
#     # 'azure': base_requirements + [requirements['azure-cognitiveservices-speech']],
#     # 'elevenlabs': base_requirements + [requirements['elevenlabs']],
#     # 'openai': base_requirements + [requirements['openai']],
#     # 'gtts': base_requirements + [requirements['gtts']],
#     # 'coqui': base_requirements + [requirements['coqui_tts']],
# }

setuptools.setup(
    name="betterscraper",
    version="0.0.1",
    author="Raj Hada",
    author_email="hammeerraj@gmail.com",
    description="Scraper for our LLM",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/criminact/betterscraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9, <3.13',
    install_requires=all_requirements,
    extras_require=extras_require,
    include_package_data=True,
    keywords='scraper, rag, python'
)