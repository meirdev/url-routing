# router_benchmarks.py

import json
import timeit

from router_radix_tree import Router as RadixTreeRouter, Routers as RadixTreeRouters
from router_regex import Router as RegExRouter, Routers as RegExRouters

radix_tree_routers = RadixTreeRouters()
regex_routers = RegExRouters()

handler = lambda *args, **kwargs: print(args, kwargs)

with open("endpoints.json") as f:
    endpoints = json.load(f)

    for method, urls in endpoints.items():
        for url in urls:
            router = RegExRouter(url, handler)
            regex_routers.add_router(method, router)

            url = url.replace("}", "")
            url = url.replace("{", ":")
            router = RadixTreeRouter(url, handler)
            radix_tree_routers.add_router(method, router)


url = "/repos/owner_X123/repo_Y123/environments/environment_name_Z123/deployment-branch-policies"

print("Random router:")
print("Radix Tree Router:", timeit.timeit("radix_tree_routers.get_handler('GET', url)", globals=globals(), number=100_000))
print("RegEx Router:", timeit.timeit("regex_routers.get_handler('GET', url)", globals=globals(), number=100_000))

url = "/orgs/org_x123/actions/cache/usage"

print("First router:")
print("Radix Tree Router:", timeit.timeit("radix_tree_routers.get_handler('GET', url)", globals=globals(), number=100_000))
print("RegEx Router:", timeit.timeit("regex_routers.get_handler('GET', url)", globals=globals(), number=100_000))
