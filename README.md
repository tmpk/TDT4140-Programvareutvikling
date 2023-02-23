# Study buddy

---
Project created by Group 99 in TDT4140

---

Build status:

Master branch:	
![alt text](https://travis-ci.org/SindreSB/TDT4140-Gruppe99.svg?branch=master "Master branch build status")

Dev branch: 	
![alt text](https://travis-ci.org/SindreSB/TDT4140-Gruppe99.svg?branch=dev "Development branch build status")


## Getting up and running

This project is build upon the Django framework using Python 3.x. Befor running this software both Python and Django must be installed. 



1) Download and unpack or clone the project.

2) Open a terminal and navigate to the project folder.

3) Run the following commang to create the local database:
```
> python manage.py migrate
```
4) (Optionally) Create a superuser/admin account by running the following command and following the prompt:
```
> python manage.py createsuperuser
```
5) Finally, run the server by executing the command 
```
> python manage.py runserver
```
6) Navigate to http://localhost:8000


## Other

#### Manual testing:

Test can be run using the Django framework's built-in test runner. Invoke the full test suite by running the 
command

```
> python manage.py test
```

For more detailed information consult the Django documentation.

#### Automated testing:

Travis-CI is used to run tests upon every commit and pull-request. 
See [the project's Travis CI page](https://travis-ci.org/SindreSB/TDT4140-Gruppe99) for test history
and branch status. The status for the master and dev branch can be seen at the top of this document.



#### Project dependencies: 
- Bootstrap 3 (v3.3)  http://getbootstrap.com/
- jQuery (Bootstrap dependency) https://jquery.com/
