---
layout: page
title: "Tutorial: an IDE for Alan"
category: docs
---

1. TOC
{:toc}

## Introduction
In this tutorial you'll get familiar with the environment for creating Alan applications.

## Application for building applications
For developing Alan applications we typically use an Integrated Development Environment (IDE): an application that provides the developer with a file and folder overview, a text editor that recognises the Alan code, and many other useful tools.
In this tutorial we'll use Visual Studio Code (VS Code) in a Chromium based browser, like Google Chrome or Microsoft Edge:

![First window](./images_IDE/001.png)

This screenshot shows the main areas in the layout:

![Basic layout](./images_IDE/002.png)

1. Explorer: overview of files and folders in your project
2. Text editor: content of open file can be edited here (on startup you'll see the `README.md` file with additional info)
3. Terminal/Output/Problems:
    - Tab 'Terminal' for executing instructions (you probably won't be needing this, but it is active by default)
    - Tab 'Output' for output from the compiler (when you want to inspect what happens when you build your project)
    - Tab 'Problems' for a nice list of issues from the compiler (this is important when errors occur)

In the top left corner you'll find these buttons:

![Icons](./images_IDE/003.png)

They determine what you see in area 1. The top icon is for the Explorer and the only one you'll need to get started.

At the bottom left side you'll see these texts:

![Texts](./images_IDE/004.png)

These are three buttons that execute important tasks:
1. Alan Fetch for downloading and updating the Alan platform tools
3. Alan Build for building your project
2. Alan Deploy for deploying your project

## Files and folders
You develop an Alan application by defining application models, defining interfaces, creating migrations, configuring settings, etc.
These activities make use of specific files within specific folders.
This structure of files and folders is required in order to compile an application.
The following files and folders are important while working on the `application` language tutorial:

![Files](./images_IDE/005.png)

The `application.alan` file in folder `models/model` contains the model of your application.
The `migration.alan` file in folder `migration/initialization` describes how your application data needs to be migrated from the current to a next version of your application.

In order to keep focus on the application language, migration files are available for each topic of the tutorial.
The location of the relevant files in the folder `_tutorials` (available in your project) can be found at the end of each topic.
By copying and pasting the migration file, your application gets some nice example data for you to experiment with.
To make sure you don't get stuck while working on the Application Language tutorial, the `_tutorials` folder contains a valid `application.alan` file for each topic as well.

## Compile and deploy
Once you've written or updated a model and want to see the result, you need to do two things:
1. Click on the button `Alan Build`.
This will build your model and check for any inconsistencies.
Errors occur if your model is not correct.
Solve any problems, until you can succesfully build your project.
2. Click on the button `Alan Deploy`.
This will send your project to the server which will publish (deploy) your application.

> NOTE: we recommend that you also run `Alan Fetch` from time to time (e.g. weekly) to get the latest platform tools for building and deploying your project. Furthermore, if you ever change the `versions.json` file, you need to run `Alan Fetch` as well to get the right tools.

## Your published Application
After deploying your work, you can find the latest published version of your application at the URL provided in the `README.md` file of your project.

More information about Visual Studio Code can be found [here](https://code.visualstudio.com/).

## Next up
Now you are all set to get started with the `application` language tutorial, which can be found [here](/pages/tutorials/application-tutorial.html). Good luck!

