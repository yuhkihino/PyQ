from django.core import validators


class StepValueValidator(validators.BaseValidator):
    message = '%(limit_value)s ‚²‚Æ‚Ì’l‚ğ“ü—Í‚µ‚Ä‚­‚¾‚³‚¢ (“ü—Í‚Í %(show_value)s)B'

    def __init__(self, limit_value, *args, **kwargs):
        if limit_value == 0:
            raise ValueError('Step value must not be zero')

        super().__init__(limit_value=limit_value, *args, **kwargs)

    def compare(self, a, b):
        return a % b
