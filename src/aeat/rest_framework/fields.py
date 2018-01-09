from rest_framework import serializers as rf


class AEATDateField(rf.DateField):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs, format='%y%m%d')


class AEATDateTimeField(rf.DateTimeField):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs, format='%Y%m%d%H%M')


class AEATTimeField(rf.TimeField):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs, format='%H%M')


class RequiredStr(rf.CharField):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs, required=True)


class NotRequiredStr(rf.CharField):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs, required=False)
