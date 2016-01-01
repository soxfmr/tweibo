# tweibo
The Crawler Of Tencent Weibo

# How to Use
## 0x1 Create your function to compose the information of the post
```python
# Initialize the data in this function
def init():
    return 0

# Take care the meta information in the data which is consist of html tag in raw
def compose(data):
    print data
    return 0
```

## 0x2 Import the function model to the main function which is located in **tweibo.py**
```python
from MyComposer import init
from MyComposer import compose
```

## 0x3 Get start to crawl the data
```
python tweibo.py
```
