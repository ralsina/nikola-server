from django.db.utils import DatabaseError

from blogs import models

def run():
    print "Saving all blogs"
    try:
        for blog in models.Blog.objects.all():
            print "=>", blog
            blog.save()
    except DatabaseError, e:
        if 'no such table' in e.args[0]:
            pass
        else:
            raise e
        
