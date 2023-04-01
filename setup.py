from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path:str) -> List[str]:
    '''
    this function will read requirements.txt file and return list of requirements
    '''
    requirements = []
    with open(file_path,'r') as f:
        for line in f:
            if HYPEN_E_DOT in line:
                requirements.append(line.replace(HYPEN_E_DOT,''))
            else:
                requirements.append(line)
    return requirements

setup(
    name='ML Package',
    version='0.0.1',
    author='Uttam Patel',
    author_email='utampipaliya@gmail.com',
    packages=find_packages(),
    description='ML Package for End to End Machine Learning Project',
    install_requires= get_requirements('requirements.txt')
)