"""Django FSM: standalone state machines and Django model state fields."""

from .base import (
    GET_STATE,
    InvalidTargetState,
    NoTransition,
    RETURN_VALUE,
    State,
    Transition,
    TransitionConditionsUnmet,
    TransitionNotAllowed,
    can_proceed,
    has_transition_perm,
)
from .chart import chart
from .this_object import this

try:
    from .fields import (
        ConcurrentTransition,
        ConcurrentTransitionMixin,
        FSMField,
        FSMFieldMixin,
        FSMIntegerField,
        FSMKeyField,
        FSMModelMixin,
        NonInitialStateOnCreate,
        transition,
    )

    _DJANGO_AVAILABLE = True
except ImportError:
    _DJANGO_AVAILABLE = False


__all__: tuple[str, ...] = (
    "TransitionNotAllowed",
    "NoTransition",
    "TransitionConditionsUnmet",
    "InvalidTargetState",
    "State",
    "this",
    "chart",
    "Transition",
    "RETURN_VALUE",
    "GET_STATE",
    "can_proceed",
    "has_transition_perm",
)

if _DJANGO_AVAILABLE:
    __all__ += (
        "FSMField",
        "FSMFieldMixin",
        "FSMIntegerField",
        "FSMKeyField",
        "FSMModelMixin",
        "ConcurrentTransition",
        "ConcurrentTransitionMixin",
        "NonInitialStateOnCreate",
        "transition",
    )


__version__ = "5.0.2"

_DJANGO_ATTRIBUTES = {
    "ConcurrentTransition",
    "ConcurrentTransitionMixin",
    "FSMField",
    "FSMFieldMixin",
    "FSMIntegerField",
    "FSMKeyField",
    "FSMModelMixin",
    "NonInitialStateOnCreate",
    "transition",
}


def __getattr__(name):
    if not _DJANGO_AVAILABLE and name in _DJANGO_ATTRIBUTES:
        raise ImportError(
            f"'{name}' requires Django to be installed. "
            "Install Django or run `pip install 'django-fsm[django]'`."
        )
    if name == "FlowAdminMixin":
        if not _DJANGO_AVAILABLE:
            raise ImportError(
                "'FlowAdminMixin' requires Django to be installed. "
                "Install Django or run `pip install 'django-fsm[django]'`."
            )
        from .admin import FlowAdminMixin

        return FlowAdminMixin
    if name == "FlowViewsMixin":
        if not _DJANGO_AVAILABLE:
            raise ImportError(
                "'FlowViewsMixin' requires Django to be installed. "
                "Install Django or run `pip install 'django-fsm[django]'`."
            )
        from .viewset import FlowViewsMixin

        return FlowViewsMixin
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
