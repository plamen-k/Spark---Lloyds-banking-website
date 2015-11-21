The html segment of the website has been written by Plamen Kolev

# Setup
Requirements:  
---
On **Windows**
1. Download git command line tool from here -> http://git-scm.com/downloads
2. Download python 2.7 from here -> https://www.python.org/ftp/python/2.7.9/python-2.7.9.msi
3. Download pip file from here -> https://bootstrap.pypa.io/get-pip.py
Pip is a package manager for python

4. Install python. After that, verify that it is in your windows path by opening a cmd terminal and type "python", if it tells you that it is not recognized, follow these instructions  
 * Right click on my computer -> properties -> on the left panel click advanced system settings -> click environmental variables on the bottom of the window -> in system variables find path -> double click it and append `;C:\Python27;C:\Python27\Scripts` to it and apply
5. Install **Pip** by changing directory in the cmd to the get-pip.py file and then type python get-pip.py install
6. After that install virtualenv by typing `pip install virtualenv`
7. Open git bash and change the directory to your local working folder (mine is 'cd Desktop\spark')
8. Clone the repository by issuing the command `git clone git@bitbucket.org:team4dev/spark.git .`, then type your private key password

## Activating the work environment
Now that we have the framework, lets' get going with the project

1. Open a cmd terminal and change directory to the working folder, mine is `cd Desktop/spark`
2. Run `virtualenv env && env\Scripts\activate && pip install django==1.7.1 pillow django-tinymce django-autofixture django-colorful djangorestframework dj_static whitenoise pytz django-periodically`
( note that in unix, activating the environment is `source env/bin/activate`)
3. Skip this if you want empty website, otherwise run `python manage.py migrate`
4. Then run  `python manage.py shell` and in the console, enter `execfile('gc.py')`
5. You can use localhost:8000/admin to access the admin panel
6. Have fun !

# Some resources

http://agiliq.com/blog/2012/06/understanding-args-and-kwargs/

For form development, a very good reference guide for advanced features
http://www.b-list.org/weblog/2008/nov/09/dynamic-forms/

For everything else, RTFM !

Forms multiple choice

http://stackoverflow.com/questions/9993939/django-display-values-of-the-selected-multiple-choice-field-in-a-template

Fill form from the view
http://stackoverflow.com/questions/1993014/passing-kwargs-to-django-form

More on forms
http://twigstechtips.blogspot.co.uk/2011/10/django-dynamic-forms-with-dynamic.html

Forms slideshow
http://www.slideshare.net/pydanny/advanced-django-forms-usage

Client server authentication
http://stackoverflow.com/questions/18330916/how-to-authenticate-android-user-post-request-with-django-rest-api

www.django-rest-framework.org

https://getblimp.github.io/django-rest-framework-jwt/ < token
