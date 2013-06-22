from blogs import models

def run():
    print "Saving all blogs"
    for blog in models.Blog.objects.all():
        print "=>", blog
        blog.save()
