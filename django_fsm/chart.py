# Copyright (c) 2017-2020, Mikhail Podgurskiy
# All Rights Reserved.

# This work is licensed under AGPL defined in file 'LICENSE' with the
# additional permissions of 'LICENSE_EXCEPTION', both part of this package.

import re
from enum import Enum
from typing import Any, List, Set, Tuple

try:
    from django.db.models import Choices
except ImportError:
    Choices = None  # type: ignore[assignment,misc]

from .utils import DEFAULT
from .base import State, StateDescriptor, Transition
from .typing import StateValue


def get_state_name(state_value: StateValue) -> str:
    if isinstance(state_value, Enum):
        return str(state_value.value)
    return str(state_value)


def get_state_label(state_value: StateValue) -> Any:
    if Choices is not None and isinstance(state_value, Choices):
        return state_value.label
    elif isinstance(state_value, Enum):
        return str(state_value.value)
    return str(state_value)


_OPENING_QUOTE = re.compile(r'(^|[\s(\[{])"')


def dot_text(value: Any) -> str:
    """Make ``value`` safe inside a double-quoted DOT string.

    DOT consumers disagree on how a quote is escaped: Graphviz wants ``\\"``,
    while the DOT parser of vis-network, which draws the charts in the browser,
    reads a backslash literally and ends the string at the quote. No escape is
    valid for both, so a double quote is replaced with a typographic one.
    """
    text = _OPENING_QUOTE.sub("\\1\u201c", str(value))
    return text.replace('"', "\u201d")


def chart(flow_state: StateDescriptor, exclude_guards=True):
    """
    Draws a directed graph (digraph) of the state transitions defined in the
    given `flow_state`.

    Args:
        flow_state (StateDescriptor): The state descriptor object.
        exclude_guards (bool): Whether to exclude transitions with no target state.

    Returns:
        str: A string representation of the digraph in the DOT language.

    The function uses the `flow_state` object to extract the transitions and the
    states involved. It then generates a DOT language string, which can be used
    with tools like Graphviz to produce an image of the graph.

    A ``State.RETURN_VALUE``/``State.GET_STATE`` target charts one edge per
    declared allowed state; if none are declared, the transition is charted
    with no outgoing edge, since its real target is only known at runtime.
    """
    vertices: Set[StateValue] = set()
    postponed: List[Transition] = []
    edges: Set[Tuple[StateValue, StateValue, Transition]] = set()

    # prepare data
    for method, transitions in flow_state.get_transitions().items():
        for transition in transitions:
            if exclude_guards and transition.target is DEFAULT:
                continue
            if transition.source == State.ANY:
                postponed.append(transition)
            else:
                vertices.add(transition.source)
                for target in transition.declared_targets():
                    vertices.add(target)
                    edges.add((transition.source, target, transition))

    # Collect every target first: a State.ANY transition has an edge from the
    # target of each other State.ANY transition, whatever the declaration order.
    for transition in postponed:
        vertices.update(transition.declared_targets())

    for transition in postponed:
        for target in transition.declared_targets():
            for vertex in vertices:
                if vertex == target:
                    continue
                edges.add((vertex, target, transition))

    # build chart
    vertices_definition = "\n".join(
        [
            '"%s" [label="%s"];'
            % (dot_text(get_state_name(vertex)), dot_text(get_state_label(vertex)))
            for vertex in sorted(vertices, key=get_state_name)
        ]
    )

    edges_definition = "\n".join(
        [
            '"%s" -> "%s" [label="%s"];'
            % (
                dot_text(get_state_name(source)),
                dot_text(get_state_name(target)),
                dot_text(transition.label),
            )
            for source, target, transition in sorted(
                edges,
                key=lambda edge: (
                    get_state_name(edge[0]),
                    get_state_name(edge[1]),
                    edge[2].label,
                ),
            )
        ]
    )

    return """digraph {
%s
%s
}""" % (
        vertices_definition,
        edges_definition,
    )
