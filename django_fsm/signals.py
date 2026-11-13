"""Signals emitted by FSM model fields; plain State transitions do not emit them."""

try:
    from django.dispatch import Signal

    pre_transition = Signal()
    post_transition = Signal()
except ImportError:
    pre_transition = None  # type: ignore[assignment]
    post_transition = None  # type: ignore[assignment]
