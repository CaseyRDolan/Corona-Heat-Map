# Corona-Heat-Map
A Dash web app based on current COVID-19 data from [worldometers.info](https://www.worldometers.info/coronavirus/). It displays current COVID-19 metrics on choropleth maps of the world and the United States. It can be used to quickly compare the spread of COVID-19 across the globe visually.
<br><br>
Built for M&T Bank's "Code for a Cause" challenge during their 2020 Technology Intern Summer Engagement Journey.

## Demo
[Working Demo](https://covidheatmap.herokuapp.com)<br>
[Informational Youtube Video](https://youtu.be/0RrtXU3A8AA)

## Technology
- [Python 3.8](https://www.python.org/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - Library for scraping web data
- [Plotly](https://plotly.com/) - Library for creating a variety of data visualization tools
- [Dash](https://plotly.com/dash/) - A web app framework for plotly graphs

## Bug Reports / Feature Requests
To report a bug, please open an issue [here](https://github.com/CaseyRDolan/Corona-Heat-Map/issues/new). Please do your best to describe what was happening when the bug occured.

To request a feature, please open an issue [here](https://github.com/CaseyRDolan/Corona-Heat-Map/issues/new) and give us your ideas for additional features!

## To-Do
- Add another graph based on data selected with the plotly lasso tool on the choropleth map.
- Add top 5 lists for each of the metrics being represented
- Add information down to the county level within the United states

## Deployment
Corona-Heat-Map is a Dash web app, which uses the Flask web framework. It can be hosted and deployed on any of the major web hosting services, ie. Azure (IIS), AWS (Elastic Beanstalk), or Google app Engine. A full list of deployment options and steps can be found here: https://flask.palletsprojects.com/en/1.1.x/deploying/

Below is a list of steps to deploy using Heroku on windows:

1. download python 3 (https://www.python.org/downloads/)
2. download git (https://git-scm.com/downloads)
3. download heroku and create an account (https://devcenter.heroku.com/articles/heroku-cli)
4. open the command prompt and go to the directory you wish to save to: Ex. Desktop
5. clone the GitHub repository using the command: git clone
6. install gunicorn: pip install gunicorn
7. cd into the project directory: cd Corona-Heat-Map
8. login to heroku within the command prompt: heroku login
9. create the app within heroku: heroku create "name"
10.push the code to heroku: git push heroku master

## Team
[Casey Dolan](https://github.com/CaseyRDolan) | [Hollis Pauquette](https://github.com/pauquette) | [Anthony DeMartino](https://github.com/AnthonyRenato) | [Navid Khan](https://github.com/Nvd09)
