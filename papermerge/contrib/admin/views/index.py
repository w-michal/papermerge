from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from papermerge.search.backends import get_search_backend
from papermerge.core.models import (
    Page,
    Folder,
    BaseTreeNode,
    Access,
)


@login_required
def browse(request):
    return render(
        request,
        "admin/index.html"
    )


@login_required
def inbox_view(request):

    try:
        inbox = Folder.objects.get(
            title=Folder.INBOX_NAME,
            user=request.user
        )
        root_node_id = inbox.id

    except Folder.DoesNotExist:
        root_node_id = None

    return render(
        request,
        "admin/index.html",
        {
            'root_node_id': root_node_id
        }
    )


@login_required
def search(request):
    # 'qa' is search term from "advanced search form"
    search_term = request.GET.get('q') or request.GET.get('qa')
    tags_list = request.GET.getlist('tag')
    backend = get_search_backend()

    results_folders = backend.search(search_term, Folder)
    results_docs = backend.search(search_term, Page)

    if results_docs:
        qs_docs = BaseTreeNode.objects.filter(
            id__in=[
                p.document.basetreenode_ptr_id for p in results_docs
            ]
        )
    else:
        qs_docs = BaseTreeNode.objects

    if tags_list:
        qs_docs = qs_docs.filter(
            tags__name__in=tags_list
        ).distinct()

    nodes_perms = request.user.get_perms_dict(
        qs_docs, Access.ALL_PERMS
    )

    qs_docs = [
        node for node in qs_docs.prefetch_related('tags')
        if nodes_perms[node.id].get(Access.PERM_READ, False)
    ]

    # filter out all documents for which current user
    # does not has read access

    return render(
        request,
        "admin/search.html",
        {
            'results_docs': qs_docs,
            'results_folders': results_folders.results(),
            'search_term': search_term,
            'tags_list': tags_list
        }
    )

