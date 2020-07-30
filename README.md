# Corona-Heat-Map
 Authors: Casey Dolan, Hollis Pauquette, Navid Khan, Anthony DeMartino
 
 Corona-Heat-Map is a Dash web app, which uses the Flask web framework.
 It can be hosted and deployed on any of the major web hosting services, ie. Azure (IIS), AWS (Elastic Beanstalk), or Google app Engine.
 A full list of deployment options and steps can be found here: https://flask.palletsprojects.com/en/1.1.x/deploying/
 
 Due to its compatibility with the Flask web framework and its relative ease of deployment, we chose to use Heroku web hosting.
 Our deployed version of the Corona-Heat-Map web app can be found here: https://covidheatmap.herokuapp.com/
 
 Below is a list of steps to deploy using Heroku on windows:
 
 1.  download python 3 (https://www.python.org/downloads/)
 2.  download git (https://git-scm.com/downloads)
 3.  download heroku and create an account (https://devcenter.heroku.com/articles/heroku-cli)
 4.  open the command prompt and go to the directory you wish to save to: Ex. Desktop
 5.  clone the GitHub repository using the command: git clone <link to the repository>
 6.  install gunicorn: pip install gunicorn
 7.  cd into the project directory: cd Corona-Heat-Map
 8.  login to heroku within the command prompt: heroku login
 9.  create the app within heroku: heroku create "name"
 10. push the code to heroku: git push heroku master



