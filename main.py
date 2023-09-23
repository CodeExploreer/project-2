from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import json

# Disable the virtual keyboard's dock mode and set it to single mode
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
Config.write()

class CollegeInfoApp(App):
    def build(self):
        self.student_info_list = []  # Initialize the list to store student info

        self.layout = BoxLayout(orientation='vertical', padding=10)

        self.name_label = Label(text="Enter Student Name:")
        self.name_input = TextInput(hint_text="Name")

        self.college_label = Label(text="Enter College Name:")
        self.college_input = TextInput(hint_text="College Name")

        self.next_button = Button(text="Next")
        self.next_button.bind(on_release=self.show_main_input)

        self.view_button = Button(text="View All Students")
        self.view_button.bind(on_release=self.view_all_students)

        self.layout.add_widget(self.name_label)
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.college_label)
        self.layout.add_widget(self.college_input)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.view_button)

        self.popup = None  # Initialize a variable to store the popup

        return self.layout

    def show_main_input(self, instance):
        name = self.name_input.text
        college = self.college_input.text

        if not name or not college:
            self.show_popup("Error", "Please fill in both Name and College fields.")
        else:
            self.create_main_input_view(name, college)

    def create_main_input_view(self, name, college):
        self.layout.clear_widgets()  # Clear the initial input view

        course_label = Label(text="Enter Course:")
        self.course_input = TextInput(hint_text="Course")

        dob_label = Label(text="Enter Date of Birth:")
        self.dob_input = TextInput(hint_text="DOB (yyyy-mm-dd)")

        phone_label = Label(text="Enter Phone Number:")
        self.phone_input = TextInput(hint_text="Phone Number")

        email_label = Label(text="Enter Gmail Address:")
        self.email_input = TextInput(hint_text="Gmail Address")

        aadhar_label = Label(text="Enter Aadhar Card Number:")
        self.aadhar_input = TextInput(hint_text="Aadhar Card Number")

        old_percentage_label = Label(text="Enter Old Year Percentage:")
        self.old_percentage_input = TextInput(hint_text="Old Year Percentage")

        submit_button = Button(text="Submit")
        submit_button.bind(on_release=self.submit_info)

        back_button = Button(text="Back")
        back_button.bind(on_release=self.show_initial_input)

        self.layout.add_widget(Label(text=f"Name: {name}\nCollege: {college}"))
        self.layout.add_widget(course_label)
        self.layout.add_widget(self.course_input)
        self.layout.add_widget(dob_label)
        self.layout.add_widget(self.dob_input)
        self.layout.add_widget(phone_label)
        self.layout.add_widget(self.phone_input)
        self.layout.add_widget(email_label)
        self.layout.add_widget(self.email_input)
        self.layout.add_widget(aadhar_label)
        self.layout.add_widget(self.aadhar_input)
        self.layout.add_widget(old_percentage_label)
        self.layout.add_widget(self.old_percentage_input)
        self.layout.add_widget(submit_button)
        self.layout.add_widget(back_button)

    def show_initial_input(self, instance):
        self.layout.clear_widgets()  # Clear the main input view
        self.layout.add_widget(self.name_label)
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.college_label)
        self.layout.add_widget(self.college_input)
        self.layout.add_widget(self.next_button)
        self.layout.add_widget(self.view_button)

    def submit_info(self, instance):
        college = self.college_input.text
        course = self.course_input.text
        name = self.name_input.text
        dob = self.dob_input.text
        phone = self.phone_input.text
        email = self.email_input.text
        aadhar = self.aadhar_input.text
        old_percentage = self.old_percentage_input.text

        if not course or not dob or not phone or not email or not aadhar or not old_percentage:
            self.show_popup("Error", "Please fill in all fields.")
        else:
            student_info = {
                "College": college,
                "Course": course,
                "Name": name,
                "DOB": dob,
                "Phone": phone,
                "Email": email,
                "Aadhar": aadhar,
                "OldPercentage": old_percentage
            }
            self.student_info_list.append(student_info)
            self.save_info()
            self.show_popup("Success", "Student information saved successfully.")
            self.create_main_input_view(name, college)  # Clear the fields for the next student

    def save_info(self):
        try:
            with open('student_info.json', 'w') as file:
                json.dump(self.student_info_list, file, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def show_popup(self, title, content):
        # Create and show a popup with the specified title and content.
        if self.popup:
            self.popup.dismiss()

        self.popup = Popup(title=title,
                           content=Label(text=content),
                           size_hint=(None, None), size=(400, 200))
        self.popup.open()

    def view_all_students(self, instance):
        if not self.student_info_list:
            self.show_popup("Info", "No student information available.")
            return

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        scroll_view = ScrollView()

        for student_info in self.student_info_list:
            student_info_label = Label(text=f"Name: {student_info['Name']}\n"
                                            f"College: {student_info['College']}\n"
                                            f"Course: {student_info['Course']}\n"
                                            f"DOB: {student_info['DOB']}\n"
                                            f"Phone: {student_info['Phone']}\n"
                                            f"Gmail: {student_info['Email']}\n"
                                            f"Aadhar: {student_info['Aadhar']}\n"
                                            f"Old Percentage: {student_info['OldPercentage']}%\n",
                                       size_hint_y=None, height=150)
            layout.add_widget(student_info_label)

        scroll_view.add_widget(layout)
        popup = Popup(title="All Students' Information",
                      content=scroll_view,
                      size_hint=(None, None), size=(500, 400))
        popup.open()

if __name__ == '__main__':
    CollegeInfoApp().run()
