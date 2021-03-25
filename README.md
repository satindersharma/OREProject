# OREProject




#### Create a virtualenv 
`virtualenv venv`


#### Activate the env

##### linux
`source venv/bin/activate`

##### window
`venv\Scripts\activate`




## Now run following commands on activated virtualenv



## Make directories if not exists
`mkdir media static templates`


#### Install required packages
`pip install -r requirements.txt`


### Run makemigrations
`python manage.py makemigrations`

### Run migrate
`python manage.py migrate`



### Create superuser
`python manage.py createsuperuser`

