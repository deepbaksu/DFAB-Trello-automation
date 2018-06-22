# DFAB-Trello-automation
It is for automatic management of DFAB Trello.  
- [Trello REST API](https://trello.readme.io/reference#introduction)
- Python3

## Automation task
The tasks are executed using `Crontab`.
1. Once a week, move cards from done list to newly created archive list(`mv_done_card.py`)
2. Create new Sprint board every month and move the necessary lists from last month's board(`create_new_board.py`)

## Architecture
```
.
|--- lib
|    |-- config.py
|    |-- logger.py
|    |-- utils.py
|    |-- query.py
|--- mv_done_card.py
|--- create_new_board.py
```

1. All functions are in `utils.py`. 
2. Configurations are in `config.py` except private variable `QUERY` in `query.py`. 
But it is **NOT** included. If you want to use this, add `query.py`. The `query.py` is like  

```python
QUERY = { "key" : "<your key>", 
          "token": "<your token>" }
```

3. Logger in `logger.py` is for logging.

## Distribution
- AWS(t2.micro, Amazon Linux)
