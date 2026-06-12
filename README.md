# Voice-Based Work Report Automation Agent

### Overview

While thinking about practical uses of AI in day-to-day operations, I noticed that many field workers and technicians spend time typing updates after completing their work. In many cases, the actual update takes less than a minute to explain verbally but several minutes to write and format into an email. The idea behind this project was to make reporting faster and more natural. Instead of typing updates, a user can simply record a voice message. The application converts the speech into text, allows the user to review and edit the transcript, generates a structured report, and sends it directly by email.

App Link: https://voice-to-report-assistant-dsr.streamlit.app/

---
### My Approach
While designing this project, I intentionally kept a human review step in the workflow instead of making the system fully autonomous. This is because speech recognition is not always perfect, so the user is given an opportunity to review and correct the transcript before any email is generated or sent.

#### Stage 1: Speech Transcription
The user records a voice note directly in the application.
Whisper is used to convert the audio into text. Before moving forward, the user can review and edit the transcript to correct any transcription errors.
The edited transcript becomes the source of truth for all downstream actions.

#### Stage 2: Report Generation
Once the transcript is approved, Gemini generates a structured report containing:
* Work completed
* Issues identified
* Safety observations
* Next steps
This converts an unstructured voice data into a consistent format that is easier to review and communicate.

#### Stage 3: Action Execution
After the report is generated, the system:
* Sends the report by email
* Automatically copies the given manager email address
* Stores the report in PostgreSQL/Supabase

This creates a complete reporting workflow while keeping the user interaction minimal.

The user only needs to record the update, review the transcript, and submit the report.

---

#### Deployment Note

The current deployment uses Gmail API with a personal Google account for demonstration purposes.

Because Gmail OAuth permissions are configured only for the project owner's account, email delivery is currently limited to the authorized Gmail account used during development.

If you are interested in using or extending this project, please feel free to connect with me. I would be happy to discuss how the email workflow can be configured for additional users, teams, or organizational environments.

---

### What the Application Does
The application takes a voice note as input and performs the following tasks:
1. Records a voice update directly in the browser
2. Converts speech into text using Whisper
3. Allows the user to review and edit the transcript
4. Generates a structured report using Gemini
5. Sends the report by email
6. Automatically copies a manager email address
7. Stores the report in a PostgreSQL database
8. Displays previously submitted reports
---
### Workflow

```text
Voice Note
      ↓
Whisper Transcription
      ↓
Transcript Review
      ↓
Gemini Report Generation
      ↓
Email Delivery
      ↓
PostgreSQL / Supabase Storage
      ↓
Report History
```
---
### Technologies Used
* Python
* Streamlit
* Whisper
* Gemini API
* Gmail API
* PostgreSQL
* Supabase
---
### Future Enhancements
Potential improvements for future versions include:
* Search and filter report history
* User authentication
* Support for user-specific email accounts through OAuth
* Additional structured fields such as site, equipment, issue type, priority, and email status
* Power BI, Tableau, or Looker Studio integration
* Dashboard reporting and trend analysis using stored report data

Pushing this product to the production environment could include additional features like:
* Role-based access control
* Approval workflows
* Audit logging
* Team-specific reporting
* Mobile support
* Integration with enterprise reporting tools

The current implementation focuses on the core workflow. The project was intentionally designed so that additional business-specific fields, reporting requirements, and integrations can be added with minimal changes to the overall architecture.

---
### Note: This is a personal portfolio project built for learning and demonstration purposes. The workflows, examples, and sample data used in the project do not represent any employer, client, or proprietary business process.

If you have ideas for improving this project, or would like to integrate it into a reporting workflow, or collaborate on future enhancements, I would be happy to connect and discuss further!
