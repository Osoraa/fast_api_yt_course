# Learning Optimal Api Architecting with Fast API

Course video is hosted on [Youtube](https://youtu.be/0sOvCWFmrtA?list=PL1rYsxRTxo1KBas9ljQv999UGGfRKx7VP)

> Using Ubuntu 22.04 for this project.

## Tools

- Code Editor
- Python3
- Postman to test requests

## Starting out

- Set up a Virtual env. for dependency management.
- Install the fastapi module/dependencies with

``` Bash
    sudo apt install python3-pip python3-venv -y

    . venv/bin/activate

    pip install fastapi[all]
```

- Start the application with

``` Bash
    uvicorn main:app --reload

```

