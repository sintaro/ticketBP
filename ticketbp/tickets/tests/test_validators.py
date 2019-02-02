from django.core.validators import ValidationError
from django.test import TestCase

from tickets import validators


class TestStepValueValidator(TestCase):
    def test_valid(self):
        target = validators.StepValueValidator(100)
        self.assertIsNone(target(100))
        self.assertIsNone(target(200))
        self.assertIsNone(target(300))

    def test_invalid(self):
        target = validators.StepValueValidator(100)

        with self.assertRaises(ValidationError):
            target(99)
        with self.assertRaises(ValidationError):
            target(101)

        with self.assertRaises(ValidationError):
            target(199)
        with self.assertRaises(ValidationError):
            target(201)

    def test_step_was_zero(self):
        with self.assertRaises(ValueError):
            validators.StepValueValidator(0)
