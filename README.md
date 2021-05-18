<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** github_username, repo_name, twitter_handle, email, project_title, project_description
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/sharmautkarsh31/hotel_power_management">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Hotel Power Management</h3>

  <p align="center">
    Manages appliances in a hotel to keep its bill in check
    <br />
    <a href="https://github.com/sharmautkarsh31/hotel_power_management"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/sharmautkarsh31/hotel_power_management">View Demo</a>
    ·
    <a href="https://github.com/sharmautkarsh31/hotel_power_management/issues">Report Bug</a>
    ·
    <a href="https://github.com/sharmautkarsh31/hotel_power_management/issues">Request Feature</a>
  </p>
</p>



[comment]: <> (<!-- TABLE OF CONTENTS -->)

[comment]: <> (<details open="open">)

[comment]: <> (  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>)

[comment]: <> (  <ol>)

[comment]: <> (    <li>)

[comment]: <> (      <a href="#about-the-project">About The Project</a>)

[comment]: <> (      <ul>)

[comment]: <> (        <li><a href="#built-with">Built With</a></li>)

[comment]: <> (      </ul>)

[comment]: <> (    </li>)

[comment]: <> (    <li>)

[comment]: <> (      <a href="#getting-started">Getting Started</a>)

[comment]: <> (      <ul>)

[comment]: <> (        <li><a href="#prerequisites">Prerequisites</a></li>)

[comment]: <> (        <li><a href="#installation">Installation</a></li>)

[comment]: <> (      </ul>)

[comment]: <> (    </li>)

[comment]: <> (    <li><a href="#usage">Usage</a></li>)

[comment]: <> (    <li><a href="#roadmap">Roadmap</a></li>)

[comment]: <> (    <li><a href="#contributing">Contributing</a></li>)

[comment]: <> (    <li><a href="#license">License</a></li>)

[comment]: <> (    <li><a href="#contact">Contact</a></li>)

[comment]: <> (    <li><a href="#acknowledgements">Acknowledgements</a></li>)

[comment]: <> (  </ol>)

[comment]: <> (</details>)



<!-- ABOUT THE PROJECT -->
## About The Project

[comment]: <> ([![Product Name Screen Shot][product-screenshot]]&#40;https://example.com&#41;)

[comment]: <> (Here's a blank template to get started:)

[comment]: <> (**To avoid retyping too much info. Do a search and replace with your text editor for the following:**)

[comment]: <> (`github_username`, `repo_name`, `twitter_handle`, `email`, `project_title`, `project_description`)


### Built With

* [Python](https://www.python.org/)
* [Django](https://docs.djangoproject.com/en/3.2/)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Things you need to use the software.
* [Python](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/installing/)
* [Postgresql11](https://www.postgresql.org/download/)



### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/sharmautkarsh31/hotel_power_management.git
   ```
   Clone and go to the root folder of the project
2. Create Python Virtual Environment <br>
   ```sh
   python3 -m venv venv
   ```
3. Activate environment 
   ```sh
   source venv/bin/activate
   ```
4. Get to the project root <br>
   ```sh
   cd hotel_electricity_management
   ```
   Run the above command and confirm that you can see `manage.py` file in current folder.
4. Install PIP packages
   ```sh
   pip install -r requirements.txt
   ```
5. Create an empty database in postgresql:<br>
   * Database name: `hotel_management`<br>
   * Role: `postgres`<br>
   * Set env variable `DB_PASSWORD` as the password that `postgres` user has.
    
6. Migrate the migrations
   ```sh
   python manage.py migrate
   ```
7. In settings.py file, change the 
    
7. Run server
   ```sh
   python manage.py runserver
   ```
    

<!-- USAGE EXAMPLES -->
## Usage

* To create hotel and its artefacts, go to http://127.0.0.1:8000/api/hotel/ and fill in the details.
* Start the management of appliances:<br>
  *Run the following command in a new terminal*
   ```sh
   python manage.py start_electricity_management
   ```
* To look at the live monitor that refreshes every 10 seconds, run following command
   ```sh
   python manage.py runscript scripts.continuous_output -v3
   ```
* To generate a movement at any Corridor, go to `http://127.0.0.1:8000/api/trigger_motion/`
 and follow along

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/sharmautkarsh31/hotel_power_management/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Utkarsh Sharma - [@twitter_handle](https://twitter.com/utkarshitis) - sharma.utkarsh31@gmail.com

Project Link: [https://github.com/sharmautkarsh31/hotel_power_management](https://github.com/sharmautkarsh31/hotel_power_management)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* []()
* []()
* []()





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/github_username