import json

from anytree import Node, RenderTree

from router_radix_tree import Router, RouterNode, Routers

routers = Routers()

handler = lambda *args, **kwargs: print(args, kwargs)

with open("endpoints.json") as f:
    endpoints = json.load(f)

    for method, urls in endpoints.items():
        for url in urls:
            url = url.replace("}", "")
            url = url.replace("{", ":")
            router = Router(url, handler)
            routers.add_router(method, router)


def draw_tree(router_node: RouterNode, node: Node):
    for child in router_node.children:
        child_node = Node(child.value, parent=node)
        draw_tree(child, child_node)


n = Node("[root]")
draw_tree(routers._routers["GET"], n)

for pre, fill, node in RenderTree(n):
    print("%s%s" % (pre, node.name))
