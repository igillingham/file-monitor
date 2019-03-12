Design Notes
============

File Monitor and Archive Service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ian Gillingham, March 2019

* A prototype service has been developed, to monitor files in a given directory and archive them after they have been dormant for a defined period (nominally 5 days).

* File metadata and archive status are maintained in a local database.

* A RESTful API has been developed for the provisioning of file data to remote clients.
 
Language and Frameworks
^^^^^^^^^^^^^^^^^^^^^^^

The factors listed above each had significant bearing on the design decisions.
The framework should facilitate:

1. Filesystem access, with a platform agnostic interface - i.e. works with most operating systems (Linux, Windows, MacOS, etc.)

2. Established database support.

3. Facilities to provide web services, both http and RESTful API.

--------------
Considerations
--------------
1. Node.js
   
   * A real contender, having good filesystem support via the 'fs' module, including file change event handling.
 
   * Good modular support for most mainstream databases, facilitating straightforward CRUD interfaces.
   
   * Using Express as a web services framework, developing a REST API would be straightforward.
   
2. Python
   * Python is often my 'goto' choice for rapid application development and prototyping, as it is mostly platform agnostic
   and a plethora of use-cases, from simple scripting, to multithreaded services, through to full featured 
   applications with various front-end interfaces. 
   
   * It has a built-in filesystem API, via os.path and able to capture events asynchronously.
   
   * Almost every database engine is supported, simply by importing the appropriate module.
   
3. Deployment

 * 3.1 Considering that the prototype system will need to be evaluated on a host, not that of the development environment, deployment is an important factor. The prototype should be deliverable in such a form that it will import all of the required dependencies and build to be as self-contained as possible. One or two caveats exist, where the target host must be configured appropriately.
    * A database server (in this case MongoDb - but this can be run locally with few privileges).

    * The facility to install a Python3 virtual environment (pipenv).
        
 * 3.2 Containerised application deployment was considered, such as:
   * Docker

   * Kubernetes

   * Ultimately it would be worth evaluating this approach, but given the present time constraints, it's necessary to compromise. This could be built upon at a later date.

4. Database

   * As a first port of call, I would typically have considered MySQL or PostgreSQL. For the sake of simplicity of deployment, it would have been significantly simpler to have adopted SQLite, which is file based and authentication is not necessary. From the list of suggested databases, I chose MongoDB, as it is straightforward to configure in a user-space environment, by simply running 'mongod'.
   
   