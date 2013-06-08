from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from fileshack.models import Store

register = template.Library()

@register.filter(name="shack_item", is_safe=True)
def shack_item(shack):

    # shack is a Fileshack Store object, it has a path like blog_id/foo/bar

    visible_path = '/'+'/'.join(shack.path.split('/')[1:])+'/'
    edit_url = reverse("fileshack:index", kwargs={"store_path":shack.path})
    add_url = reverse("store_add", kwargs={"parent_path":shack.path})

    template = """
            <li>
                <div class="btn-group">
                <a class="btn" data-toggle="modal" data-target="#modal-shack-{shack_id}"><i class="icon-folder-open"></i> {visible_path}</a>
                </div>
                <div style="width:900px; margin-left: -450px;" id="modal-shack-{shack_id}" class="modal hide fade" tabindex="-1" role="dialog">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                        <h3>{visible_path}</h3>
                    </div>
                    <div class="modal-body">
                    <form class="form-inline" action="{add_url}" method="POST">
                        <label>New Subfolder:</label>
                        <div class="input-prepend">
                            <span class="add-on">{visible_path}</span>
                            <input type="text" name="path" id="path">
                            </input>
                        </div>
                        <input type="submit" value="Create">
                    </form>

                    <iframe src="{edit_url}" style="border: none; width: 880px; margin: -10px;height: 600px;"></iframe>
                    </div>
                </div>
            </li>
""".format(visible_path=visible_path, edit_url=edit_url, shack_id=shack.id, add_url=add_url)

    return mark_safe(template)

@register.filter(name="sub_shacks", is_safe=True)
def sub_shacks(shack):
    children = Store.objects.filter(path__startswith=shack.path+"/")
    return mark_safe('\n\n'.join([shack_item(shack) for shack in children]))
