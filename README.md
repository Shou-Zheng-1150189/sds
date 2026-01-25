Selwyn Dance School (SDS) Web Application

COMP636 – Web Application Development

Project Overview

Selwyn Dance School (SDS) is implementing a web-based internal administration system.
The system is intended solely for staff usage and allows them to manage students, classes, enrolments, and examine basic reports.

The application is created with Python, Flask, MySQL, SQLite (as provided for COMP636) and Bootstrap, adhering to the limitations and recommended practices covered in COMP636.

Authorship Statement

I completed this project on my own for the COMP636 evaluation.

Throughout the project's development, I employed AI-assisted tools such as ChatGPT and GitHub Copilot. These tools were used for:

Clarify Flask's routing and template rendering principles

Help with debugging Python, SQL, and deployment issues.

Help structure HTML templates with Bootstrap.

Enable form validation logic and error handling.

Provide instructions for PythonAnywhere deployment and configuration.

I thoroughly studied, tested, and understood all of the code.
I can describe and justify the design and implementation decisions taken throughout this project.
The image used on the homepage was generated using ChatGPT (OpenAI) for educational purposes only.

Design Decisions

Throughout the application's development, the following design considerations were made:

I utilized Flask with function-based routes to make the application basic, legible, and in line with the course requirements.

All other templates used and expanded a common base.html template to guarantee that the header, navigation bar, and footer were uniform across all pages.

To avoid code duplication, I reused the /students route for both listing and searching students, utilizing a query parameter (q).

Lists of student names provide clickable links to the student class summary page, which improves usability and navigation efficiency.

Separate routes and templates were designed for adding and editing students in order to keep validation logic simple and avoid complex conditional templates.

In accordance with typical web development standards, GET requests are used to show forms and POST requests to submit and process data.

The database automatically generates student IDs to preserve data integrity and avoid disputes.

Server-side validation is used on all forms to avoid invalid input, such as missing names or future dates.

The enrolling function limits class choices to eligible classes depending on the student's current grade level, enforcing business rules at the app level.

SQL queries were constructed with parameterized placeholders (?) to avoid SQL injection and assure secure database interaction.

The class list and student summary pages make use of similar SQL joins to ensure consistent sorting and rapid data retrieval.

No student or class data is hard-coded; all data is dynamically obtained from the database to ensure that the application is compatible with various datasets used during marking.

Image Resources

The image seen on the homepage was：

Generated with AI tools, ChatGPT.

The image is used solely for educational purposes and meets the project's image usage guidelines.

Database Question

The present app does not save information about parents or caregivers.

To assist parents with several children enrolled at the dancing school, I would set up a new parents booth as well as a connection table between parents and pupils. This would allow a single parent to be associated with several students without duplicating information.

This architecture enables data normalization and would allow for future additions such as parent login access, shared contact information, and consolidated billing while keeping existing student records intact.

Technologies Used:

Python

Flask

MySQL

Bootstrap (CSS Only)

To meet the COMP636 standards, no additional JavaScript frameworks or new CSS were employed.

Deployment

The application is hosted on PythonAnywhere and synchronized with a private GitHub repository.
All essential routes and functionalities work properly in the hosted environment.

Notes

This application was created entirely utilizing the technologies taught in COMP636 and adheres to all evaluation limitations involving structure, validation, and deployment.
