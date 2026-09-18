import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question


def create_question(question_text, days):
    return Question.objects.create(
        question_text=question_text,
        pub_date=timezone.now() + datetime.timedelta(days=days),
    )


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        question = create_question("Future question", days=30)
        self.assertIs(question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        question = create_question("Old question", days=-1.1)
        self.assertIs(question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        question = create_question("Recent question", days=-0.5)
        self.assertIs(question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay encuestas disponibles")
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [],
        )

    def test_past_question_is_visible(self):
        question = create_question("Past question", days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, question.question_text)

    def test_future_question_is_not_visible(self):
        question = create_question("Future question", days=1)
        response = self.client.get(reverse("polls:index"))
        self.assertNotContains(response, question.question_text)

    def test_past_and_future_questions_only_show_past(self):
        past = create_question("Past question", days=-1)
        future = create_question("Future question", days=1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [past],
        )
        self.assertNotContains(response, future.question_text)

    def test_questions_are_newest_first_and_limited_to_five(self):
        questions = [
            create_question(f"Question {index}", days=-(index + 1))
            for index in range(6)
        ]
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            questions[:5],
        )


class QuestionDetailViewTests(TestCase):
    def test_past_question_is_available(self):
        question = create_question("Past question", days=-1)
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)

    def test_future_question_returns_404(self):
        question = create_question("Future question", days=1)
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertEqual(response.status_code, 404)


class QuestionResultsViewTests(TestCase):
    def test_past_question_results_are_available(self):
        question = create_question("Past question", days=-1)
        Choice.objects.create(question=question, choice_text="Yes", votes=2)
        response = self.client.get(reverse("polls:results", args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Yes")
        self.assertContains(response, "2")

    def test_future_question_results_return_404(self):
        question = create_question("Future question", days=1)
        response = self.client.get(reverse("polls:results", args=(question.id,)))
        self.assertEqual(response.status_code, 404)


class VoteViewTests(TestCase):
    def test_valid_vote_increments_choice_and_redirects(self):
        question = create_question("Past question", days=-1)
        choice = Choice.objects.create(
            question=question,
            choice_text="Yes",
            votes=0,
        )

        response = self.client.post(
            reverse("polls:vote", args=(question.id,)),
            {"choice": choice.id},
        )

        self.assertRedirects(
            response,
            reverse("polls:results", args=(question.id,)),
        )
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 1)

    def test_missing_choice_rerenders_detail_with_error(self):
        question = create_question("Past question", days=-1)
        choice = Choice.objects.create(
            question=question,
            choice_text="Yes",
            votes=0,
        )

        response = self.client.post(reverse("polls:vote", args=(question.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No seleccionaste una opción.")
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 0)

    def test_invalid_choice_rerenders_detail_with_error(self):
        question = create_question("Past question", days=-1)

        response = self.client.post(
            reverse("polls:vote", args=(question.id,)),
            {"choice": 999999},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No seleccionaste una opción.")

    def test_future_question_cannot_be_voted(self):
        question = create_question("Future question", days=1)
        choice = Choice.objects.create(
            question=question,
            choice_text="Yes",
            votes=0,
        )

        response = self.client.post(
            reverse("polls:vote", args=(question.id,)),
            {"choice": choice.id},
        )

        self.assertEqual(response.status_code, 404)
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 0)

    def test_missing_question_returns_404(self):
        response = self.client.post(
            reverse("polls:vote", args=(999999,)),
            {"choice": 1},
        )
        self.assertEqual(response.status_code, 404)
