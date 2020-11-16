# binary_reverse.py

Binary reverse file project

### Setup
In order to use **binary_reverse.py** cli you need following **tools** installed:

* python3.7
    
    * Mac:
        ``` sh
        brew install python3.7
        ```
    * Linux:
        ``` sh
        sudo apt install python3.7
        ```
    * Windows:
        ``` sh
        choco install python --version=3.7.1
        ```          
* pip
    ``` sh
    python -m pip install -U pip
    ```
* pipenv:
    ``` sh
    pip install pipenv
    ```
<br/>
If you want to change default ENV variable behaviour you can check this on app/env.py file:

* LOG_LEVEL: The console logging level INFO|DEBUG. default: INFO

* OUTPUT_FILE_PREFIX: Output reverse binary file prefix. default: "reverse-"


### Install
For dependencies management we use **Pipfile** with **pipenv** cli:
``` sh
pipenv install
```

### Run
Run **binary_reverse** cli inside pipenv environment:

``` sh
pipenv shell && pipenv install && python -m binary_reverse [file1, file2 ... ]
```

### Test
For the current functionality the project contains just integration tests. To run this execute:
``` sh
python -m unittest discover -v -s tests/integration
```

***
This README had been created by **pancudaniel7**
