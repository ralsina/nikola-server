To deploy Alva in your own Debian or Ubuntu server:

* Install ansible in your computer
* In your server, setup the alva database in MySQL with some user and password granted full access
* Copy deployment.yml.example to deployment.yml
* Edit it and use real names and passwords
* Edit hosts in the obvious way
* Run something like this (change as needed): ansible-playbook ansible/deployment.yml -u root -i hosts 
