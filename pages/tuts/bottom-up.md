---
layout: page
title: "Alan Bottom Up"
category: docs
---

In this article we'll take a look at how everything in Alan connects, from the bottom up.


## Server

A typical Alan runtime environment, e.g. as provided by our standard ISO, looks like this:

	╔══════════════════════════════════════╗
	║[            alan server             ]║
	║[   linux kernel + some core utils   ]║  <- or macOS, Ubuntu 16.04+, etc
	╚══════════════════════════════════════╝

We depend on a number of Unix utilities, so Alan runs on top of a tiny custom Linux distro. The initial Alan layer provides a basic infrastructure server to interact with. 

When you deploy an [image](#image) to the server, it will pull additional runtimes from the cloud based on information in that image. This creates the final runtime "stack". For a basic project, this includes:

- Alan Operating System (orchestrates interaction between systems).
- Runtimes for each system type:
  - datastore
  - reporter
  - webclient

Systems in the stack can expose interfaces, but otherwise stacks are isolated containers running on top of the server:

	┌────────────── stack A ───────────────┐
	│[ datastore ][ reporter ][ webclient ]│
	│[        alan operating system       ]│
	└──────────────────────────────────────┘
	╔══════════════════════════════════════╗
	║[            alan server             ]║
	║[   linux kernel + some core utils   ]║
	╚══════════════════════════════════════╝


## Image

An "image" for deployment contains data for each system and configuration for the runtime environment. This includes ports, scheduled tasks, etc. An image also contains a versions list, telling the server which runtimes to download. 

The image also contains the [project package](#project), which (via the wiring) tells the alan operating system how all the systems should talk to each other.

So, you can think of the image as the complete set of instructions for the server to create the stack you've designed.

You compile an image using `./alan package <project.pkg> <deployment>`, i.e. by combining the project package with a deployment configuration.


	┌────────────── image ───────────────┐
	| deployment.alan                    │
	│ system instance data               │
	│ data migration packages            │
	│ runtime ("minor") versions         │
	│                                    │
	│ ┌─────────── project ────────────┐ │
	│ │ wiring.alan                    │ │
	│ │ shared interface configuration │ │
	│ │ system configuration           │ │
	│ │ design time ("major") versions │ │
	│ └────────────────────────────────┘ │
	└────────────────────────────────────┘


## Project

A project contains the "source code" for the systems you want to use, and a configuration for how the systems are wired together. E.g. the server provides data that the client then consumes. When you bootstrap a project, Alan downloads the specifications for each system-type, that tell us exactly what each system can provide or consume. 

When two systems talk to each other, they do so based on a shared specification or "interface". These specifications are in the shared directory.

In the systems directory you find each system, each with their own configuration. The reporter system type has queries for each report, the webclient has some settings like the display name of your application and the datastore can define how to implement external interfaces.

You compile a project using `./alan build`, resulting in the project.pkg that's the basis for creating an [image](#image).


## A word about versions

You'll have noticed the versions.json at the root of your project. It defines a set of systems and platform that should be compatible. New builds of system version X is guaranteed to be based on the exact same language and configuration, but may contain bugfixes. We call these "major" versions.

The project.pkg contains this versions list, to ensure that each next step uses the same major versions as your design.

The package step adds a "minor" version for each system-type. Systems speak a set of protocols amongst each other and that need to match. We have a mapping that tells the package utility what minor versions are correct for your project. New builds of system version X.Y are guaranteed to speak the same protocols. 

Finally there is a "patch" level of versioning, for which we simply use build id's. Alan's core tool chain guarantees that at this level compatibility cannot be broken, so it's always safe to use the latest builds. The Alan stack manager tool helps you upgrade systems to get the latest bug fixes.
