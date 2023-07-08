<a name="readme-top"></a>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="https://www.powerflex.com/wp-content/themes/powerflex/img/logo-white.svg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Sprocket Factory REST API</h3>

  <p align="center">
    sprocket service for consuming and process sprocket factory information!
    <br />
    <br />
    <a href="https://www.postman.com/alfredojonas/workspace/powerflex-challenge/overview">Postman Collection</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

### Api Design

![Api design][api-design]

### ERD Design

![ERD][erd]

#### Task:
- [] Build a RESTful api that services requests for sprocket factory data and sprockets.
- [] The app should be built using either Python (3.9+) or Typescript.
- [] For data retention, a database or cache can be used.
- [] Ideally, use docker/docker-compose for standing up the datastore.
- [] The code should be on a github repository that should be shared with your engineering contact.

#### RESTful Endpoints
- [] An endpoint that returns all sprocket factory data
- [] An endpoint that returns factory data for a given factory id
- [] An endpoint that returns sprockets for a given id
- [] An endpoint that will create new sprocket
- [] An endpoint that will update sprocket for a given id
- [] Seed data/examples of the factory and sprocket are in the attached JSON files
- [X] Include a README with instructions on how to stand up the database and application



<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With


* [![Django][django]][django-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

This is a dockerized project, in terms of build this up you'll need to have already installed and configured Docker on your machine.
* <a href="https://docs.docker.com/desktop/?_gl=1*16tppjw*_ga*MTM2MTA3NTk5NC4xNjg1OTE4NTA0*_ga_XJWPQMJYHQ*MTY4NzI3MTMzMy4xMi4xLjE2ODcyNzEzNjkuMjQuMC4w">Install and configure Docker</a>

### Installation

_You can follow this steps in order to have an app build and up._

1. Clone this repo
   ```sh
   git clone https://github.com/AlfredoJonas/powerflex-sprockets-factory-api
   ```
2. Move on the root dir of your project
    ```sh
    cd powerflex-sprockets-factory-api
    ```
3. Do a copy of the *env.example* file renaming it as *.env*
   ```sh
   cp .env.example .env
   ```
4. Now just build the app using docker, in this case we encapsuled all the required steps in a single makefile command, so just type...
   ```sh
   make appsetup
   ``` 
5. Run tests to confirm everything is OK
    ```sh
    docker-compose run sprocket-api pytest
    ```
6. To lift the app use docker as usual running
    ```sh
    docker-compose up
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Jonas Gonzalez - [@Sanoj94](https://twitter.com/Sanoj94) - alfredojonas94@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Resources I find helpful and would like to give credit to.

* [Django docs](https://docs.djangoproject.com/en/4.2/)
* [Docker for django admin](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples)
* [PyTests on Django](https://pytest-django.readthedocs.io/en/latest/)
* [StackOverflow](https://stackoverflow.com/)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[django]: https://img.shields.io/badge/Django-103e2e?style=for-the-badge&logo=django&logoColor=white
[django-url]: https://www.djangoproject.com/
[system-design]: DataModelAndSystemChart.png
[api-design]: api-design.svg
[erd]: ERD.svg