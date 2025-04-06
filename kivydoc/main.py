from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from datetime import datetime, timedelta
from calendar import monthcalendar, month_name
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import calendar
from calendar import month_name
from kivy.app import App


Builder.load_file('homepage.kv')
Builder.load_file('appointment.kv')
Builder.load_file('profile.kv')


class AppointmentScreen(Screen):
    pass
class ProfileScreen(Screen):
    pass

class HomepageScreen(Screen):
    current_date = datetime.now()
    selected_date = None
    selected_time_slots = set()  # Store blocked slots


    def on_kv_post(self, base_widget):
        self.show_current_month()
        self.update_calendar()

    def show_current_month(self):
        self.ids.month_year.text = f"{month_name[self.current_date.month]} {self.current_date.year}"

    def update_calendar(self):
        grid = self.ids.calendar_grid
        grid.clear_widgets()

        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for day in days:
            grid.add_widget(Label(text=day, bold=True, font_size='12sp', color=(0, 0, 0, 1)))

        today = datetime.now().date()
        cal = monthcalendar(self.current_date.year, self.current_date.month)

        for week in cal:
            for day in week:
                if day == 0:
                    grid.add_widget(Label(text=''))
                else:
                    date_obj = datetime(self.current_date.year, self.current_date.month, day).date()
                    is_past_date = date_obj < today
                    btn = Button(
                        text=str(day),
                        size_hint_y=None,
                        height=dp(40),
                        background_normal='',
                        background_color=(1, 1, 1, 1) if date_obj != self.selected_date else (0.2, 0.6, 1, 1),
                        color=(0.2, 0.2, 0.2, 1),
                        bold=True,
                        disabled=is_past_date
                    )
                    if not is_past_date:
                        btn.bind(on_press=lambda instance, d=day: self.show_time_slots(d))
                    grid.add_widget(btn)

        self.hide_time_slots()

    def prev_month(self):
        self.current_date = self.current_date.replace(day=1) - timedelta(days=1)
        self.current_date = self.current_date.replace(day=1)
        self.show_current_month()
        self.update_calendar()

    def next_month(self):
        self.current_date = self.current_date.replace(day=28) + timedelta(days=4)
        self.current_date = self.current_date.replace(day=1)
        self.show_current_month()
        self.update_calendar()

    def show_time_slots(self, day):
        self.selected_date = datetime(self.current_date.year, self.current_date.month, day).date()
        self.update_calendar()

        self.ids.time_layout.clear_widgets()
        self.selected_time_slots.clear()

        # "Select All" checkbox
        select_all_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        select_all_label = Label(text="Select All", size_hint_x=0.8)
        select_all_checkbox = CheckBox(size_hint_x=0.2)
        select_all_checkbox.bind(active=self.toggle_select_all)
        select_all_layout.add_widget(select_all_label)
        select_all_layout.add_widget(select_all_checkbox)
        self.ids.time_layout.add_widget(select_all_layout)

        start_time = datetime.strptime('09:00', '%H:%M')
        end_time = datetime.strptime('18:00', '%H:%M')
        interval = timedelta(minutes=15)

        now = datetime.now()

        self.selected_time_slot = None

        while start_time <= end_time:
            slot_time = start_time.strftime('%I:%M %p')
            is_past_time = (self.selected_date == now.date() and start_time.time() <= now.time())
            btn = Button(
                text=slot_time,
                size_hint=(1, None),
                height=dp(40),
                background_color=(0.02, 0.1, 0.4, 1) if not is_past_time else (0.5, 0.5, 0.5, 1),
                color=(1, 1, 1, 1),
                disabled=is_past_time
            )
            btn.bind(on_press=lambda instance, t=start_time: self.select_time_slot(instance, t))
            self.ids.time_layout.add_widget(btn)
            start_time += interval

        Clock.schedule_once(self.adjust_time_slots_height)

    def show_time_slots(self, day):
        self.selected_date = datetime(self.current_date.year, self.current_date.month, day).date()
        self.update_calendar()

        self.ids.time_layout.clear_widgets()
        self.selected_time_slots.clear()

        # "Select All" checkbox
        select_all_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        select_all_label = Label(text="Select All", size_hint_x=0.8)
        select_all_checkbox = CheckBox(size_hint_x=0.2)
        select_all_checkbox.bind(active=self.toggle_select_all)
        select_all_layout.add_widget(select_all_label)
        select_all_layout.add_widget(select_all_checkbox)
        self.ids.time_layout.add_widget(select_all_layout)

        start_time = datetime.strptime('09:00', '%H:%M')
        end_time = datetime.strptime('18:00', '%H:%M')
        interval = timedelta(minutes=15)

        now = datetime.now()

        while start_time <= end_time:
            slot_time = start_time.strftime('%I:%M %p')
            is_past_time = (self.selected_date == now.date() and start_time.time() <= now.time())
            btn = Button(
                text=slot_time,
                size_hint=(1, None),
                height=dp(40),
                background_color=(0.02, 0.1, 0.4, 1) if not is_past_time else (0.5, 0.5, 0.5, 1),
                color=(1, 1, 1, 1),
                disabled=is_past_time
            )
            if not is_past_time:
                btn.bind(on_press=lambda instance, t=start_time: self.toggle_time_slot(instance, t))
            self.ids.time_layout.add_widget(btn)
            start_time += interval

        if not hasattr(self, 'confirm_button'):
            self.confirm_button = Button(
                text='Confirm',
                size_hint=(1, None),
                height=dp(40),
                background_color=(0.02, 0.1, 0.4, 1),
                color=(1, 1, 1, 1)
            )
            self.confirm_button.bind(on_press=self.confirm_blocked_slots)
            self.ids.time_container.add_widget(self.confirm_button)
        self.confirm_button.opacity = 1

        Clock.schedule_once(self.adjust_time_slots_height)

    def toggle_time_slot(self, instance, time):
        """Allow multiple selections of time slots"""
        if time in self.selected_time_slots:
            self.selected_time_slots.remove(time)
            instance.background_color = (0.02, 0.1, 0.4, 1)
        else:
            self.selected_time_slots.add(time)
            instance.background_color = (1, 0, 0, 1)

    def toggle_select_all(self, checkbox, value):
        """Select or deselect all time slots"""
        self.selected_time_slots.clear()
        for widget in self.ids.time_layout.children:
            if isinstance(widget, Button):
                if value:
                    widget.background_color = (1, 0, 0, 1)
                    self.selected_time_slots.add(widget.text)
                else:
                    widget.background_color = (0.02, 0.1, 0.4, 1)

    def confirm_blocked_slots(self, instance):
        """Save the blocked slots for the selected date"""
        if self.selected_time_slots:
            print(f"Blocked slots on {self.selected_date}: {sorted(self.selected_time_slots)}")
            #  store  blocked slots in a database
        else:
            print("No slots selected")

    def hide_time_slots(self):
        self.ids.time_layout.clear_widgets()
        self.ids.time_container.size_hint_y = None
        self.ids.time_container.height = 0
        self.ids.time_container.opacity = 0

    def adjust_time_slots_height(self, *args):
        self.ids.time_layout.height = self.ids.time_layout.minimum_height
        self.ids.time_container.size_hint_y = None
        self.ids.time_container.height = self.ids.time_layout.height + dp(50)
        self.ids.time_container.opacity = 1

class QuestionScreen(Screen):
    pass

class MainApp(MDApp):
    months = [month_name[i] for i in range(1, 13)]  # List of months

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(HomepageScreen(name='homepage'))
        self.screen_manager.add_widget(ProfileScreen(name='profile'))
        self.screen_manager.add_widget(AppointmentScreen(name='appointment'))


        return self.screen_manager

    def switch_screen(self, screen_name):
        self.screen_manager.current = screen_name

if __name__ == '__main__':
    MainApp().run()
