from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.dropdown import DropDown


class SpinnerOptions(SpinnerOption):

    def __init__(self, **kwargs):
        super(SpinnerOptions, self).__init__(**kwargs)
        self.background_normal = ""
        self.background_color = [0.3, 0.2, 1, 0.7]
        self.height = self.height * 0.8
        self.font_size = self.width / 10 + 2


class SpinnerDropdown(DropDown):

    def __init__(self, **kwargs):
        super(SpinnerDropdown, self).__init__(**kwargs)
        self.auto_width = True
        self.width = self.width 


class SpinnerWidget(Spinner):
    def __init__(self, **kwargs):
        super(SpinnerWidget, self).__init__(**kwargs)
        self.dropdown_cls = SpinnerDropdown
        self.option_cls = SpinnerOptions