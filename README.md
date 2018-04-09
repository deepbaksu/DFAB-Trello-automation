# DFAB-Trello-automation
This is for automatic management of DFAB Trello.  
- [Trello REST API](https://trello.readme.io/reference#introduction)
- python3

## Automation task
1. Once a week, move cards from done list to newly created archive list(`mv_done_card.py`)
2. Create new Sprint board every month and move the necessary lists from last month's board(`create_new_board.py`)

## Architecture
1. All functions are in `utils.py` 

2. Configurations are in `config.py` except private variable `QUERY` in `query.py`. 
But it is **NOT** included. If you want to use this, add `query.py`. The `query.py` is like  

```python
Query = { "key" : "<your key>", 
          "token": "<your token>" }
```



3. Logger in `logger.py` is for logging.
