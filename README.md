<img width="1440" alt="Home Page" src="https://github.com/user-attachments/assets/4dcf24f0-dc4b-4d4f-9726-01f797db13fd">Safe NT

This project was developed for the IT Code Fair challenge, organized by Charles Darwin University (CDU). Our team of four — Sujan Kandel, Sushant Regmi, Vipashyana Guni, and Rachit Adhikari — collaborated to build this project using the Django web framework.

Project Overview

Safe NT is designed to provide essential security and medical support through a web platform. It features four different access levels with unique functionalities:

Normal User - Access to book medical appointments and report incidents.
Doctor - Schedule management, appointment approval, and patient check-ups.
Police - Incident monitoring, alert response, and incident history.
Admin - Account verification for doctors and police officers.
This system allows users to book appointments with doctors and directly report incidents to the police. A critical feature is the camera-based gesture detection for emergencies, using user cameras temporarily, with future plans to integrate NT surveillance cameras.

Key Features

Medical Appointment System:
Users can book an appointment with doctors at their preferred time.
Doctors can approve appointments and manage their availability.

Incident Reporting:
Users can file a case directly with the police through the website.
Police have a dashboard to view and respond to incidents.

Emergency Gesture Detection:
A machine learning model detects a five-finger gesture to signal distress.
Upon detecting this gesture, the system sends a notification with a real-time photo to the police.
Designed to work even if the user has no phone, enabling prompt police response.

Account Verification:
Admins verify and activate police and doctor accounts to ensure security and authenticity.
Technology Stack

Backend: Django (Python web framework)
Frontend: HTML, CSS, JavaScript (integrated within Django templates)
Machine Learning: Gesture detection model (five-finger distress signal)
Access Credentials

For testing purposes, use the following credentials to log in:

Admin:
Username: admin
Password: qwe123Q!
Police:
Username: police
Password: qwe123Q!
Doctor:
Username: doctor, doctor1, doctor2, etc.
Password: qwe123Q!
Patient:
Username: patient
Password: qwe123Q!
Note: You can create your own user accounts after cloning the repository.


Setup and Installation
To set up this project locally:

Clone the repository:
git clone <repository-url>

Install dependencies:
pip install -r requirements.txt

Run migrations:
python manage.py migrate

Start the Django development server:
python manage.py runserver

Open your browser and navigate to http://127.0.0.1:8000.


Demo and Screenshots:
<img width="1440" alt="Home Page" src="https://github.com/user-attachments/assets/2ebe074c-ea38-48cd-9f8d-4612f13019e0">
<img width="1440" alt="Login page" src="https://github.com/user-attachments/assets/f53c053c-cf78-43a8-bc46-eefb66be9b38">
<img width="1440" alt="Patient Home" src="https://github.com/user-attachments/assets/d1507277-1e1b-45c9-91df-60d5cfc28bc8">
<img width="1440" alt="Doctors List" src="https://github.com/user-attachments/assets/73e8e184-1aa4-4573-95cf-c85089aebc0e">
<img width="1440" alt="Doctors Dashboard" src="https://github.com/user-attachments/assets/f0a4f90a-2e27-4dfd-acac-10f1ca92f7ed">
<img width="1440" alt="Police Dashboard" src="https://github.com/user-attachments/assets/ebea0caf-9c59-4217-a058-d56d7ab15adb">
<img width="1440" alt="Mobile Detetection" src="https://github.com/user-attachments/assets/4dcd6625-e713-4c88-91d1-5f456b2bd58d">


You can view a demo video on YouTube showcasing the user experience and addressing security issues in the Northern Territory: https://youtu.be/BvaLfllWc6w

Future Enhancements

Full integration with NT's camera system to enable real-time emergency detection in high-risk areas.
Enhanced machine learning capabilities for improved accuracy in gesture recognition and quicker response times.

Contributors

Sujan Kandel      : s360707
Sushant Regmi     : s358630
Vipashyana Guni   : s359308
Rachit Adhikari   : s359140
