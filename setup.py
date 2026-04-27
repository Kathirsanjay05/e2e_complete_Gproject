from setuptools import find_packages,setup # type: ignore
from typing import List

HYPEN_E_DOT = '-e .'
FILE_PATH = 'requirements.txt'



def get_requirements(file_path:str)->List[str]:

    '''
    This function will read and return the requirements packages

    '''

    requirements=[]
    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [i.replace("\n","") for i in requirements] 

    if HYPEN_E_DOT in requirements:
        requirements.remove(HYPEN_E_DOT)

    return requirements



## like a metadata 
setup(
    name='complete_e2e_project',
    version='0.0.1',
    author='kathir sanjay',
    author_email='kathirsanjay5@gmail.com',
    packages = find_packages(), # it directly go and see every folder and folder which 
    # has __init__.py it directly consider the folder(src) as package and build this 
    install_requires = get_requirements(file_path=FILE_PATH)
)