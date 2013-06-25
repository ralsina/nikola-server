To deploy Alva in your own Debian or Ubuntu server:

* In your server, setup the alva database in MySQL with a user and password granted access
* Copy deployment.yml.example to deployment.yml
* Edit it and use real names and passwords
* Edit hosts in the obvious way
* Run something like this (change as needed): ansible-playbook ansible/deployment.yml -u root -i hosts 
