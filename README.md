# Toolsuite for the TSG Reutlingen Fencing Department
Regular, standardizes workflows can be automated by programms and scripts. This repo holds a collectoion of such programms and scripts, that aim to automate all of such workflows that can occur while managing the fencing department of the TSG Reutlingen sports club.

**Disclaimer:** The projects developed in this repositiory are not officialy comissioned by the club. Deveopment started because I (Max) wanted to automate the processes to have less manual work to do.

## Overview
As all projects are relatively small in size and scope, the descition was made to keep them together in a single repository. This leads to more challenges in e.g. the CI pipelines, as it has to be ensured that a given pipeline does not affect other projects. On the other hand it removes the overhead of starting a project codeing common data structures and patterns _from scratch_, as code, tools and workflows can be reused over multiple projects.

The repository currently contains these projects:

+ ophardt_to_excel: Convert data-files from the ophartd system to excel files.
+ saison-kickstarter: Automate the creation of overviews that are used to plan the saison.
+ kickstart-gui: A graphical, web-based user interface to interact with the saison-kickstarter software.

## Tooling
Following is a table that lists the tools and their usecases in the project. Please note, that this only lists tools that are used across sub-projects. Other tools like for example test-frameworks and / or third-party libraries are listed in their respective subdirectories.

| Tool           | Usecase                                                                                                                               |
|----------------|---------------------------------------------------------------------------------------------------------------------------------------|
| Python         | Dynamically typed programming language. Used to develop scripts and automate tasks.                                                   |
| github         | The platform used to host the source code.                                                                                            |
| github actions | Define 'workflows' as CI pipelines.<br>These pipelines can be used to build excecutable artifacts and run quality checks on the code. |
| Typescript     | A programing language based of JavaScript that provides types annotations. Used in different frameworks to develop web interfaces.    |
| ReactJS        | Framework to build UI components for web-based guis. Uses typescript as its programing language.                                      |

