# Toolsuite for the TSG Reutlingen Fencing Department
Regular, standardizes workflows can be automated by programms and scripts. This repo holds a collectoion of such programms and scripts, that aim
to automate all of such workflows that can occur while managing the fencing department of the TSG Reutlingen sports club.

**Disclaimer:** The projects developed in this repositiory are not officialy comissioned by the club. Deveopment started because I (Max) wanted to 
automate the processes to have less manual work to do.

## Overview
As all projects are relatively small in size and scope, the descition was made to keep them together in a single repository. This leads to
more challenges in e.g. the CI pipelines, as it has to be ensured that a given pipeline does not affect other projects. On the other hand it
removes the overhead of starting a project codeing common data structures and patterns _from scratch_, as code, tools and workflows can be
reused over multiple projects.

The repository currently contains these projects:

+ ophardt_to_excel: Convert data-files from the ophartd system to excel files.
