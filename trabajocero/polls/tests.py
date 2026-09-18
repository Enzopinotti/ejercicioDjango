import datetime
from pathlib import Path

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


class TemplateAccessibilityTests(TestCase):
    def setUp(self):
        self.question = create_question("Accessible question", days=-1)
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="Yes",
            votes=1,
        )

    def test_maintained_pages_define_mobile_viewport_and_main_landmark(self):
        urls = [
            reverse("polls:index"),
            reverse("polls:detail", args=(self.question.id,)),
            reverse("polls:results", args=(self.question.id,)),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(
                    response,
                    '<meta name="viewport" content="width=device-width, initial-scale=1">',
                    html=True,
                )
                self.assertContains(response, "<main", count=1)

    def test_vote_form_groups_choices_and_labels_inputs(self):
        response = self.client.get(
            reverse("polls:detail", args=(self.question.id,))
        )
        self.assertContains(response, "<fieldset")
        self.assertContains(response, "<legend>Opciones de respuesta</legend>")
        self.assertContains(
            response,
            f'id="choice-{self.choice.id}"',
        )
        self.assertContains(
            response,
            f'for="choice-{self.choice.id}"',
        )
        self.assertContains(response, "required")

    def test_vote_error_is_announced(self):
        response = self.client.post(
            reverse("polls:vote", args=(self.question.id,))
        )
        self.assertContains(
            response,
            '<p id="vote-error" role="alert">No seleccionaste una opción.</p>',
            html=True,
        )

    def test_results_use_spanish_vote_singular_and_plural(self):
        plural = Choice.objects.create(
            question=self.question,
            choice_text="No",
            votes=2,
        )
        response = self.client.get(
            reverse("polls:results", args=(self.question.id,))
        )
        self.assertContains(response, "1 voto")
        self.assertContains(response, "2 votos")
        self.assertNotContains(response, "1 votos")
        self.assertContains(response, plural.choice_text)

    def test_results_without_choices_describe_missing_options(self):
        question = create_question("No choices", days=-1)
        response = self.client.get(
            reverse("polls:results", args=(question.id,))
        )
        self.assertContains(
            response,
            "No hay opciones disponibles para esta encuesta.",
        )


class StaticAccessibilityTests(TestCase):
    def test_styles_expose_keyboard_focus_and_reduced_motion_contracts(self):
        from django.contrib.staticfiles import finders

        path = finders.find("polls/style.css")
        self.assertIsNotNone(path)
        source = Path(path).read_text(encoding="utf-8")
        self.assertIn(":focus-visible", source)
        self.assertIn("prefers-reduced-motion: reduce", source)


class AdminContractTests(TestCase):
    def test_question_and_choice_models_remain_registered(self):
        from django.contrib import admin

        self.assertIn(Question, admin.site._registry)
        self.assertIn(Choice, admin.site._registry)

    def test_anonymous_admin_requires_login(self):
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])
