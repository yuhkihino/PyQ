from django import forms

from . import models


class ProfileEditForm(forms.ModelForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # �S�Ẵt�B�[���h��K�{�ɂ���
        for k in self.fields:
            self.fields[k].required = True

    class Meta:
        model = models.User
        fields = (
            'last_name',
            'first_name',
            'address1',
            'address2',
        )
