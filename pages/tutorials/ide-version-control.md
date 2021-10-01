---
layout: page
head: "Alan IDE: version control & offline editing"
title: "Alan IDE:<br>version control<br> & offline editing"
category: docs
---

1. TOC
{:toc}

## Introduction
This guide explains how to **set up version control** with Git for Alan IDE projects.
It also explains how to [**collaborate with others**](#collaborating-with-others) using an existing Git repository.
If you do not know what version control is, we encourage you to just use the online Alan IDE and skip this guide.

If you are comfortable using Git and want to use your own editor/develop when offline, please follow the instructions from this guide.

## Generate an SSH key
Generate an SSH key for the Alan IDE.
We recommend that you do not use your own private key, but generate one instead as shown below.
For details on SSH, see [this guide](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

- From the **Terminal** in the Alan IDE environment, run
```sh
ssh-keygen -t ed25519 -C "<user>@<domain>.<ext>"
```
and **just press Enter** when asked for a *file* and a *passphrase*\*, unless you know exactly what you are doing. <sup>*Please note that if you do provide a passphrase, you may experience issues with Git integration in VS Code.</sup>

- Copy the contents of the public key file to your clipboard:
```
cat ~/.ssh/id_ed25519.pub # contents of public key file
```


## Git hosting provider
Now, head to [GitHub](https://github.com/) or another hosting provider for Git.
- Add your public key to your account.
- Create a new repository like `my-alan-project`.


## Files to Git
Go back to the online IDE.
Run these commands from the **Terminal**:
```sh
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
git init
git add .
git commit -m "first commit"
git remote add origin git@github.com:<username>/my-alan-project.git
git push
```


## Working locally
Now you can clone the repository on your local machine:
```sh
git clone git@github.com:<username>/my-alan-project.git
```

VS Code users can find the Alan extension [here](https://marketplace.visualstudio.com/items?itemName=Kjerner.alan).
Emacs users can find *AlanForEmacs* [here](https://github.com/alan-platform/AlanForEmacs).

Please note that for deploying your Alan project (`Alan Deploy`), you will still need the online environment (Alan IDE).
If you want/need to be able to deploy locally, please request this on the [forum](https://forum.alan-platform.com) or send us an email.
If we receive a significant number of requests, we will add a guide for local deployments.


## Collaborating with others
You can collaborate with others using an existing Git repository by following the steps below.
- Generate an SSH key as explained [here](#generate-an-ssh-key), and add the public key your account.
- Configure your username and email address for Git, by running the following commands from the **Terminal** in the Alan IDE environment:

```sh
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```

- For a private repository, ask someone to add you as a collaborator.
- Make sure that the repository does not contain the `./deployments` directory.
	If it does: remove it and add `/deployments/*` to the `.gitignore` file. *
- Then, run the following commands from the **Terminal** in the Alan IDE environment:

```sh
cd ~/project
git init .

# commit your own project
git checkout -b my-own-branch
git add .
git commit . -m "own initial commit"

# add remote repository
git remote add origin git@github.com:<username>/my-alan-project.git
git fetch origin
git checkout master # or other branch from teammate
```


\* Deployments are your own: `./deployments/*/deployment.alan` files contain your Alan app url/ide name.
If you overwrite your deployments with those of someone else, you need to update your `deployment.alan` files.
You can do that by replacing all occurences of the `<name-of-someone-else>` with `<your-ide-name>`.