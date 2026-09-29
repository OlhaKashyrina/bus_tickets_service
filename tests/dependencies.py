from collections.abc import Callable

from fastapi import FastAPI
from starlette.routing import Mount


def override_dependency(app: FastAPI, dependency: Callable, override: Callable) -> None:
    app.dependency_overrides[dependency] = override

    for route in app.router.routes:
        if isinstance(route, Mount):
            route.app.dependency_overrides[dependency] = override


def clear_dependency_override(app: FastAPI, dependency: Callable) -> None:
    app.dependency_overrides.pop(dependency, None)

    for route in app.router.routes:
        if isinstance(route, Mount):
            route.app.dependency_overrides.pop(dependency, None)
