import re
from enum import Enum
from unittest import TestCase

from django.db import models

import django_fsm as fsm
from django_fsm import State
from django_fsm.chart import dot_text


class TestFlow:
    state = fsm.State(states=["A", "B", "C"])

    @state.transition(source="A", target="B")
    def transition1(self):
        pass

    @state.transition(source="B", target="C")
    def transition2(self):
        pass

    @state.transition(source="A", target="C")
    def transition3(self):
        pass


class Test(TestCase):
    def test_chart(self):
        output = fsm.chart(TestFlow.state)
        expected_output = """digraph {
"A" [label="A"];
"B" [label="B"];
"C" [label="C"];
"A" -> "B" [label="Transition1"];
"A" -> "C" [label="Transition3"];
"B" -> "C" [label="Transition2"];
}"""
        self.assertEqual(output.strip(), expected_output.strip())


class NoTargetFlow:
    # A "self-transition" that runs a side-effecting function without
    # changing state -- target is left at its DEFAULT sentinel, not None.
    state = fsm.State(states=["A", "B"])

    @state.transition(source="A", target="B")
    def advance(self):
        pass

    @state.transition(source="A")
    def touch(self):
        pass


class TestNoTargetTransition(TestCase):
    def test_no_target_transition_does_not_draw_a_default_vertex(self):
        # BUG: chart() tested `transition.target is None`, but the runtime's
        # actual "no target / unchanged" sentinel is the DEFAULT marker, not
        # None. A transition left with no explicit target (the DEFAULT
        # marker) was therefore drawn as a real "DEFAULT" vertex/edge.
        output = fsm.chart(NoTargetFlow.state)

        self.assertNotIn("DEFAULT", output)
        self.assertIn('"A" [label="A"];', output)
        self.assertIn('"B" [label="B"];', output)
        self.assertIn('"A" -> "B" [label="Advance"];', output)

    def test_explicit_none_target_is_rejected(self):
        # The runtime treats an explicit `target=None` as "set state to
        # None" (state.set(instance, None) runs, since None is not the
        # DEFAULT sentinel), while chart() used to silently drop it as if
        # it were "no target". That disagreement is exactly what produced
        # the DEFAULT-vertex bug above. `target=None` is ambiguous with
        # "no target" (the DEFAULT sentinel) is spelled by simply omitting
        # `target`, so reject the explicit None outright.
        state = fsm.State(states=["A", "B"])

        with self.assertRaises(ValueError):

            class _Flow:
                state.transition(source="A", target=None)(lambda self: None)


class Stage(Enum):
    NEW = "new"
    PUBLISHED = "published"
    REMOVED = "removed"


class EnumFlow:
    state = fsm.State(Stage, default=Stage.NEW)

    @state.transition(source=Stage.NEW, target=Stage.PUBLISHED)
    def publish(self):
        pass

    # Same source/target as publish: forces the edge sort to compare two
    # Transition objects.
    @state.transition(source=Stage.NEW, target=Stage.PUBLISHED)
    def republish(self):
        pass

    # State.ANY marker as the source.
    @state.transition(source=State.ANY, target=Stage.REMOVED)
    def remove(self):
        pass


class TestEnumChart(TestCase):
    def test_chart_with_enum_states_and_any_marker(self):
        # Regression for #476: Enum members and State.ANY markers are not
        # orderable, so sorting vertices/edges must not rely on their __lt__.
        output = fsm.chart(EnumFlow.state)
        self.assertIn("digraph {", output)
        self.assertIn('label="Publish"', output)
        self.assertIn('label="Republish"', output)
        self.assertIn("removed", output)


def parse_dot(output):
    """Split chart() output into declared vertex ids and edge endpoints.

    Every body line must be a well-formed vertex or edge statement, so a stray
    quote inside a name or label fails the parse.
    """
    vertex_line = re.compile(r'^"([^"]*)" \[label="([^"]*)"\];$')
    edge_line = re.compile(r'^"([^"]*)" -> "([^"]*)" \[label="([^"]*)"\];$')
    vertices, edges = {}, []
    lines = output.strip().splitlines()
    assert lines[0] == "digraph {" and lines[-1] == "}", output
    for line in lines[1:-1]:
        if not line:
            continue
        match = vertex_line.match(line)
        if match:
            vertices[match.group(1)] = match.group(2)
            continue
        match = edge_line.match(line)
        assert match, f"malformed DOT line: {line!r}"
        edges.append(match.groups())
    return vertices, edges


class TestEnumEdges(TestCase):
    def test_edges_connect_the_declared_vertices(self):
        # Vertices were named by the Enum member's value ("new"), while the
        # edges used str(member) ("Stage.NEW"), so no edge touched a vertex
        # and the diagram was drawn with disconnected nodes.
        vertices, edges = parse_dot(fsm.chart(EnumFlow.state))

        self.assertIn(("new", "published", "Publish"), edges)
        self.assertIn(("new", "removed", "Remove"), edges)
        for source, target, _ in edges:
            self.assertIn(source, vertices)
            self.assertIn(target, vertices)

    def test_text_choices_edges_are_unchanged(self):
        class Status(models.TextChoices):
            NEW = "new", "New"
            DONE = "done", "Done"

        class ChoicesFlow:
            state = fsm.State(Status, default=Status.NEW)

            @state.transition(source=Status.NEW, target=Status.DONE)
            def finish(self):
                pass

        vertices, edges = parse_dot(fsm.chart(ChoicesFlow.state))

        self.assertEqual(vertices, {"done": "Done", "new": "New"})
        self.assertEqual(edges, [("new", "done", "Finish")])


class AnyFlow:
    state = fsm.State(states=["new", "mid", "x", "y"], default="new")

    @state.transition(source="new", target="mid")
    def go(self):
        pass

    @state.transition(source=State.ANY, target="x", label="To X")
    def to_x(self):
        pass

    @state.transition(source=State.ANY, target="y", label="To Y")
    def to_y(self):
        pass


class ReversedAnyFlow:
    # The same transitions, but the method names list "y" before "x": state
    # transitions are enumerated by method name, not by declaration order.
    state = fsm.State(states=["new", "mid", "x", "y"], default="new")

    @state.transition(source="new", target="mid")
    def go(self):
        pass

    @state.transition(source=State.ANY, target="y", label="To Y")
    def a_to_y(self):
        pass

    @state.transition(source=State.ANY, target="x", label="To X")
    def b_to_x(self):
        pass


class TestAnySource(TestCase):
    def test_any_transitions_reach_each_other(self):
        # Edges of a State.ANY transition were built from the vertices known
        # at that moment, so a target of the next ANY transition was missed:
        # "x -> y" was drawn but "y -> x" was not.
        _, edges = parse_dot(fsm.chart(AnyFlow.state))

        self.assertIn(("x", "y", "To Y"), edges)
        self.assertIn(("y", "x", "To X"), edges)
        for vertex in ("new", "mid"):
            self.assertIn((vertex, "x", "To X"), edges)
            self.assertIn((vertex, "y", "To Y"), edges)
        self.assertNotIn(("x", "x", "To X"), edges)

    def test_chart_does_not_depend_on_the_order_of_transitions(self):
        self.assertEqual(fsm.chart(AnyFlow.state), fsm.chart(ReversedAnyFlow.state))


class QuotedFlow:
    state = fsm.State(states=["new", 'say "ok"'], default="new")

    @state.transition(source="new", target='say "ok"', label='Say "hi"')
    def speak(self):
        pass


class TestQuotes(TestCase):
    def test_double_quotes_keep_the_graph_well_formed(self):
        # `[label="Say "hi""]` is not valid DOT. No escape works for every
        # consumer (Graphviz wants \", the vis-network parser reads the
        # backslash literally and ends the string), so quotes are replaced
        # with typographic ones.
        vertices, edges = parse_dot(fsm.chart(QuotedFlow.state))

        self.assertEqual(edges, [("new", "say “ok”", "Say “hi”")])
        self.assertIn("say “ok”", vertices)
        self.assertIn("new", vertices)

    def test_text_without_quotes_is_untouched(self):
        self.assertEqual(dot_text("Re-publish: A/B (x)"), "Re-publish: A/B (x)")
        self.assertEqual(dot_text('a"b'), "a”b")
        self.assertEqual(dot_text('"a" and ("b")'), "“a” and (“b”)")
