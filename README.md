⸻


# Selwyn Dance School (SDS) Web Application  
*COMP636 – Web Application Development*

---

## Project Overview

Selwyn Dance School (SDS) is implementing a web-based internal administration system.  
The system is intended solely for staff usage and allows them to manage students, classes, enrolments, and examine basic reports.

The application is created using Python, Flask, SQLite (as provided for COMP636 and PythonAnywhere), and Bootstrap, adhering to the limitations and recommended practices covered in COMP636.

---

## Authorship Statement

I completed this project on my own for the COMP636 evaluation.

Throughout the project's development, I employed AI-assisted tools such as *ChatGPT* and *GitHub Copilot*. These tools were used to:

- Clarify Flask routing and template rendering principles  
- Assist with debugging Python, SQL, and deployment issues  
- Help structure HTML templates using Bootstrap  
- Support form validation logic and error handling  
- Provide guidance for PythonAnywhere deployment and configuration  

I thoroughly studied, tested, and understood all of the code.  
I can describe and justify the design and implementation decisions taken throughout this project.

The image used on the homepage was generated using ChatGPT (OpenAI) for educational purposes only.

---

## Design Decisions

Throughout the application's development, the following design decisions were made:

- Flask function-based routes were used to keep the application simple, readable, and aligned with course requirements.
- All templates extend a common base.html to ensure consistent navigation and layout.
- The /students route was reused for both listing and searching students using a query parameter (q) to reduce duplication.
- Student names are displayed as clickable links to improve navigation and usability.
- Separate templates were created for adding and editing students to keep validation logic simple.
- GET requests are used to display forms, while POST requests handle form submissions.
- Student IDs are generated automatically by the database to preserve data integrity.
- Server-side validation is applied to prevent invalid input such as missing names or future dates.
- Enrolment logic restricts available classes based on a student’s current grade level.
- Parameterized SQL queries (?) are used to prevent SQL injection.
- SQL joins are structured consistently across list and summary views.
- No student or class data is hard-coded; all content is dynamically retrieved from the database.
- The teacher report was implemented as a separate route and template to improve separation of concerns.
- NZ-style date formatting is applied at the template level using a Flask filter.

---

## Image Resources

- Homepage image generated using *ChatGPT (OpenAI)*  
- Image is used for educational purposes only

---

## Database Question

The current application does not store information about parents or caregivers.

To support parents with multiple children enrolled at the school, I would introduce a separate *Parents* table and a *parent–student relationship table*.  
This design would allow one parent to be linked to multiple students without duplicating information.  
It also supports future enhancements such as shared contact details, parent logins, and consolidated billing while maintaining data normalization.

---

## Technologies Used

- Python  
- Flask  
- SQLite (as provided for COMP636 and PythonAnywhere)  
- Bootstrap (CSS only)

No additional JavaScript frameworks or custom CSS were used, in accordance with COMP636 requirements.

---

## Deployment

The application is hosted on *PythonAnywhere* and synchronized with a private GitHub repository.  
All required routes and functionality operate correctly in the hosted environment.

---

## Notes

This application was developed entirely using the technologies taught in COMP636 and adheres to all assessment constraints regarding structure, validation, and deployment.


⸻
