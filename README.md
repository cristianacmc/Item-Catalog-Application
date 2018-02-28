# ITEM CATALOG APPLICATION


### OVERVIEW
> This application provides a list of modalities within a variety of sports as well as provide a user registration and authenthication system.

### Getting Started
There are some dependencies that should be download in order to run the project:

1. Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
2. Create a `catalog` folder inside of the vagrant folder
3. Clone the repository https://github.com/cristianacmc/Item-Catalog-Application.git inside the catalog folder
4. From the terminal launch the Vagrant VM (type `vagrant up`)
5. Log into Vagrant VM (type `vagrant ssh`)
6. Go to the directory `cd/vagrant/catalog`
7. Setup the database by typing `python database.py` from the terminal
8. Populate the database by running `python categories.py`
10. Run the application by typing `python application.py` into the Terminal
11. Access the application by visiting `http://localhost:8000` locally on your browser

### Google Login
For the Google login to work you need to follow these additional steps:

1. Access [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'Catalog Application'
7. Authorized JavaScript origins = 'http://localhost:8000'
8. Authorized redirect URIs = 'http://localhost:8000' && 'http://localhost:5000/gconnect'
9. After Creating Copy the Client ID and paste it into the `data-clientid` in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file `catalog` directory 
14. Run application `python application.py` and login in the main page










