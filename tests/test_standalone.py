import unittest
from enum import Enum
import django_fsm as fsm


class ReviewState(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Review:
    state = fsm.State(ReviewState, default=ReviewState.DRAFT)

    @state.transition(source=ReviewState.DRAFT, target=ReviewState.PUBLISHED)
    def publish(self):
        pass

    @state.transition(source=ReviewState.PUBLISHED, target=ReviewState.ARCHIVED)
    def archive(self):
        pass

    @state.transition(
        source=ReviewState.DRAFT,
        target=ReviewState.ARCHIVED,
        conditions=[lambda instance: False],
    )
    def reject(self):
        pass


class StandaloneFSMTest(unittest.TestCase):
    def test_state_flow(self):
        review = Review()
        self.assertEqual(review.state, ReviewState.DRAFT)

        self.assertTrue(fsm.can_proceed(review.publish))
        self.assertFalse(fsm.can_proceed(review.reject))

        review.publish()
        self.assertEqual(review.state, ReviewState.PUBLISHED)

        # Cannot publish again
        self.assertFalse(fsm.can_proceed(review.publish))
        with self.assertRaises(fsm.TransitionNotAllowed):
            review.publish()

        # Direct assignment is blocked
        with self.assertRaises(AttributeError):
            review.state = ReviewState.ARCHIVED

        review.archive()
        self.assertEqual(review.state, ReviewState.ARCHIVED)

    def test_chart_generation(self):
        dot = fsm.chart(Review.state)
        # vertices and the edges between them use the same Enum value names
        for name in ("draft", "published", "archived"):
            self.assertIn(f'"{name}" [label="{name}"];', dot)
        self.assertIn('"draft" -> "published" [label="Publish"];', dot)
        self.assertIn('"published" -> "archived" [label="Archive"];', dot)
        self.assertNotIn("ReviewState", dot)


if __name__ == "__main__":
    unittest.main()
