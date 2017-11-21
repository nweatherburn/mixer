# Welcome to my JobCoin implementation!

Author: Nick Weatherburn
Date: 21/11/2017
Supported Language: >Python3.6

## Blurb

The majority of the work happens in `mixer.py` and `jobs.py`. 
Database object definitions are stored in `models.py`.
Relevant settings are in 

## Setup

1. Make sure that mixer_address has at least 50 jobcoin.
2. _(optional)_ Create a virtualenv environment with python3. 
    `virtualenv env -p python3`
    `source env/bin/activate`
    Confirm that `python --version` is a version of python >3.6
3. `pip install -r requirements.txt`
4. `python jobcoin.py`
5. _(In a separate environment)_ `python run_test.py`

## API

`http://localhost:8080/mixer/address`.

#### POST 

```
[
    {
        "address":"Address One"
    },
    {
        "address":"Address Two"
    },
    ...
]
```

