# Intro to Cybersecurity

> **IMPORTANT:** I am currently in the process of transferring everything from
> my old repository over to this one. At the moment, this repo isn't entirely
> ready for use; I will remove this notice once it's closer to completion.
>
> In addition, this repository _does not_ contain lecture materials or source
> for the course website. Those will be published in a separate repository when
> they're ready.

This repository contains the lab environments and exercises used for the Fall
2022 section of the University of Virginia's *CS3710: Introduction to
Cybersecurity*, taught by Will Shand.

## How to use this repository

To get started with using the images in this repository, you should create a
`.env` file by copying `.env.example` and filling the variables with whatever
configuration options you'd like to use.

### Building images

You can use `docker compose` to build the images. For example, the following
command (which should be run from the repository's root) builds the images for
the TickTock web app:

```bash
docker compose --project-directory . --file compose/ticktock.yml build
```

These images will be built under the repository specified by the `DOCKER_REPO`
variable of your `.env` file.

## Related repositories

I have two other repositories for the two programming assignments that students
received for the course:

- Programming Assignment 1 (Web Fuzzing):
  [kernelmethod/xfuzz](https://github.com/kernelmethod/xfuzz)
- Programming Assignment 2 (Cryptography):
  [kernelmethod/age-notebook](https://github.com/kernelmethod/age-notebook)

## FAQ

### Who is this repository for?

First and foremost, I've set it up for my own convienience :) However, I suspect
that many other educators may also find the resources in this repository
helpful.
