# router_regex_example.py

from router_regex import Router, Routers

routers = Routers()

routers.add_router("GET", Router("/users", lambda: None))
routers.add_router("GET", Router("/users/{user_id}", lambda user_id: print(f"Hi {user_id}")))
routers.add_router("GET", Router("/users/{user_id}/items/{item_id}", lambda user_id, item_id: print(f"Hi {user_id}, item {item_id}")))

if handler := routers.get_handler("GET", "/users/123/items/456"):
    handler()
else:
    print("Not found")
