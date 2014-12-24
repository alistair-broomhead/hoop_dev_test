Hoop-Dev-Test
========================

This is my solution to the following problem:

    We’d like you to construct a simple database that stores the dummy events in the accompanying CSV file. Once that’s complete, design and build a simple API that allows a third party service to interact with the records stored.

    API Operations:

        Event List:
        
            Returns a list of multiple events, and the following fields, for a specific ‘location’

             - eventID
             - name
             - category

            Being able to specify which field to order the Event List by would also be beneficial.

        Event:
        
            Returns all the data on file for a specific ‘eventID’
            
        Updates:
        
            We’ll also need to be able to update the event information from time to time. You should feel free to decide whether this is done via an API operation for via a CMS. You should be able to explain your decision.

    Deliverables:

     - All source code must be provided along with instructions of how to run it.
     - You should be prepared to talk through your approach in a follow up meeting

Quick Start
-----------

This assumes that you have already installed and configured postgres - this project can be run without it, but psycopg2 is included in the django-toolbelt package which makes heroku deployment much easier, and psycopg2 will not install without a working postgres setup. Installers are available for windows, under linux you should be able to use your distribution's package manager, and under osx you should be able to brew install it.

    cd $(SOURCE_TREE_ROOT)
    virtualenv venv                 # Set up a virtualenv for the project
    . venv/bin/activate             # Activate the virtualenv
    pip install -r requirements.txt # Install dependencies
    python manage.py syncdb         # This set up the db and add some credentials to use for auth
    python manage.py test           # Run the tests (make sure everything works in the target environment)
    python manage.py runserver      # Start a development server

You should now be able to open your browser to http://localhost:8000/rest/ and browse the API. You will find the database pre-populated with the example data and by logging in using the auth you specified at the syncdb step you can add events in the http://localhost:8000/rest/event/ endpoint using the HTTP POST method. I chose to use API methods over a CMS as it would allow for programmatic/bulk input, and allows for a CMS to be added on top later, however I have restricted this to require authentication to perform anything other than read operations.

Even quicker start
------------------

Open your browser to http://hoop-eng-test-al.herokuapp.com/rest