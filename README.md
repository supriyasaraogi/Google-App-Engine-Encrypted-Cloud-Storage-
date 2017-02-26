# Google-App-Engine-Encrypted-Cloud-Storage-
Designed a web interface in Python using Flask micro-framework to allow users to upload and fetch password protected files using AES encryption to Google Cloud Storage bucket.

Scaling a web service
On Google App Engine:
Created a web service that allows a user to login, and upload pictures, with comments. Multiple users may use this
service, and upload their pictures, comments and see others pictures. Users should be able to remove their
pictures. Use a NoSQL database for performance.
restricted picture sizes and limit number of pictures per user.

Scaling:
On App Engine, allowed multiple users to use the service simultaneously.
Measured the time taken for components (Web services, database, program logic, network)
Used jmeter (or similar) to stress test and validate your analysis.
