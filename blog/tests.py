from django.test import TestCase
from blog.models import Article,Comment
# Create your tests here.

'''
1
  3
    6
    9
  7
2
  4
    8
  5
10

'''

# comment_list = [
#     {"id":1,"content":"...","pid":None},
#     {"id":2,"content":"...","pid":None},
#     {"id":3,"content":"...","pid":1},
#     {"id":4,"content":"...","pid":2},
#     {"id":5,"content":"...","pid":2},
#     {"id":6,"content":"...","pid":3},
#     {"id":7,"content":"...","pid":1},
#     {"id":8,"content":"...","pid":4},
#     {"id":9,"content":"...","pid":3},
#     {"id":10,"content":"...","pid":None},
# ]
'''
comment_list = [
    {"id":1,"content":"...","pid":None,children_list=[]},
    {"id":2,"content":"...","pid":None,children_list=[]},
    {"id":3,"content":"...","pid":1,children_list=[]},
    {"id":4,"content":"...","pid":2,children_list=[]},
    {"id":5,"content":"...","pid":2,children_list=[]},
    {"id":6,"content":"...","pid":3,children_list=[]},
    {"id":7,"content":"...","pid":1,children_list=[]},
    {"id":8,"content":"...","pid":4,children_list=[]},
    {"id":9,"content":"...","pid":3,children_list=[]},
    {"id":10,"content":"...","pid":None,children_list=[]},
]
'''

# for comment in comment_list:
#     comment["children_list"]=[]
#
# for i in comment_list:
#     if i["pid"]:
#         Article.objects.filter(nid=i["pid"]).first().children_list.append(i)
#     else:


comment_list = Comment.objects.all().values("nid","content","parent_id")
print(comment_list)






