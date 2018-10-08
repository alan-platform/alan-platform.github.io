---
layout: page
title: "Introducing Alan"
category: docs
---


Today I’d like to introduce you to Alan. We’ve been working on it, in some capacity or other, for more than a decade. What took us so long? Well it turns out that this particular rabbit hole is kinda deep. Let me give you the short version.


## What is it?

<img src="alan.png" alt="Alan logo" width="128" height="128" style="float:right;">Alan is a [low code platform][low-code], enabling efficient and low cost development of tailor-made software applications. However, unlike typical low code platforms, you don't wire together ready-made blocks of functionality. Instead, Alan achieves low-code-ness by letting you write a different, more purposeful kind of code. It’s declarative and not [Turing complete][turing-complete], and in a way you might think of it more as configuration than programming.

In Alan [your code][model] specifies the data structure of your application. This specification defines all possible states of the data, and in effect all possible states of your application. A few lines of specification take the place of thousands of lines of code, and you will never have to touch or go near the underlying runtime code (you can’t actually).

It’s easy enough to work with for “citizen developers”, so that anyone can build tools to support their activities without needing IT  or external developer support. Having a small effective code base also means that Alan scales up to large enterprise applications without the cost and risk involved with traditional solutions.


## But how?

It all started with a desire to close the gap between requirement and implementation. What if we could specify requirements in a way that computers can understand and automatically translate into software? There would be no more need for separate, error-prone implementation efforts. Applications would by definition adhere to their specification, and they would be easy to adjust and maintain. 

Furthermore, applications would be easier to use, because they would be generated with excellent UX baked in, and implementations cannot introduce magical or unintended behavior. People would also never need training for new applications: they would already know how to use them.

It’s nice to dream isn’t it?


## A data spec for the ages

We discovered that for data centric applications (which is essentially most software you use from day to day), all application-specific state and all possible state transitions could be represented as a data structure. We no longer looked at data as something to put into a database, query and then transform into what an application actually needs. In fact, a comprehensive specification of all data that an application deals with should be sufficient for solving most typical data management problems.

Alan is the realization of this idea: at its heart it’s a data modeling language that enables detailed specification of data. With Alan you can specify all possible states of an application, and all possible state transitions. In addition, you can describe calculations, access control, and data transformations to share data with external systems. 


## Fully generated push architecture

A data model is all you need for generating a full software stack. This includes a [graph database][graph-db] with a 100% push architecture and a responsive web-based user interface, Excel and CSV export features, and real time syncing with a SQL database.

If you need custom logic or data wrangling, Alan employs what we call “side apps”. These are small utilities that run alongside your core application. You specify what what data is available to such apps, and the operations they can perform. This ensures data security and removes the risk of inadvertently breaking side apps when modifying the core application.

Updating Alan software through new insights, or simply to add new features, is super easy. You modify the data model, specify data migration rules between the two versions, and deploy it with only a minute or two downtime and the guarantee that you won’t lose any data. If you have a brilliant idea you can have it built and deployed before your coffee gets cold.


## Well , that’ll never work...
Actually, it kinda already does.

Solutions built with Alan include everything from [small accounting systems][hours] you can build in an afternoon, to large ERP solutions. [M-industries][m-i] and [Kjerner][kjerner] have been using Alan for several years, to provide solutions for customers like [Tata Steel][tata] and [Hydro][hydro]. Alan software is being used as an integral part of day-to-day operations at large manufacturing plants, running stand-alone or as part of an infrastructure with legacy software, relational databases, and other third party systems. It includes both fully generated and custom built graphical user interfaces and dashboards, running on desktops, touch terminals, hand-held devices etc.

In practice, Alan picks up right where Excel starts to cause more problems than it solves, or where you can’t find an off-the-shelf application fitting your needs. If you need multiple users and access control, care about data quality, or want to incrementally develop an application without breaking everything all the time, Alan is what you’re looking for.


## See it with your own eyes

We understand it’s pretty unbelievable, so that’s why you can try it for yourself right now. Start from scratch by following [our tutorial][101], or take our [Hours application][hours] for a spin. Feel free to use Alan for personal projects or tools for your team. It’s still heavily under development (we still have *so* many cool ideas!), so new releases aren’t guaranteed to be backwards compatible, but stability is usually pretty good.

Want to know more about enterprise level systems, our integration tools, or about building custom UI’s with Alan? [Get in touch][contact] and ask for a demo. 

Let us know what you think on the [forum][forum] and don't be afraid to ask questions.

We’re super excited to see what you build with Alan. 


[low-code]: https://en.wikipedia.org/wiki/Low-code_development_platforms
[turing-complete]: https://en.wikipedia.org/wiki/Turing_completeness
[graph-db]: https://en.wikipedia.org/wiki/Graph_database
[model]: /pages/docs/model/36/application/grammar.html
[m-i]: https://www.m-industries.com
[kjerner]: https://www.kjerner.com/ssn/
[hours]: https://github.com/M-industries/Hours
[tata]: https://www.tatasteel.com
[hydro]: https://www.hydro.com
[101]: http://127.0.0.1:4000/pages/tuts/getting-started.html
[contact]: /about/#m-industries
[forum]: https://forum.alan-platform.com
