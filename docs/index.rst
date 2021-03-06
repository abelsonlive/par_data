.. particle documentation master file, created by
   sphinx-quickstart on Wed Dec 25 21:19:20 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

**particle**: track article promotion
========

**NOTE**: particle is no longer supported. All functionality will be replaced and enhanced by `NewsLynx <http://newslynx.org>`_.

**particle** is a tool for collecting data about the promotion of articles on **Twitter**, **Facebook**, **Webpages**, and **RSS feeds** (for now). It automatically joins this data together by a common url and bucketed timestamp.  This enables analysis similar to that which I discuss in this `blog post <http://brianabelson.com/open-news/2013/11/14/Pageviews-above-replacement.html>`_. ``particle`` is the ideal companion to `pollster <https://github.com/stdbrouw/pollster>`_, which tracks the `performance` of links on social media.

Quickstart
----------

**particle** runs off of a ``yaml`` or ``json`` config file (or simply a ``python`` dictionary) which contains information about the data sources you want to collect. If you want to see an example of such a file, check out `this one <http://github.com/abelsonlive/particle/blob/master/examples/nytimes/nytimes.yml>`_, or go straight to the `configuration documentation <config.html>`_.

When you start a new ``particle`` project, you'll want to indicate where this file is::

  from particle import Particle

  p = Particle('particle.yml')

This one function will set up your ``particle`` project and deal with any necessary authentication with external API's (more on all this in the `configuration documentation <config.html>`_.

Now you're all set to run ``particle``::

  p.run()

Alternatively, you can run this same sequence of functions via the command line interface:

.. code-block:: bash
  
  $ particle run -c particle.yml

Now put ``particle`` on a ``cron`` and let it go!

.. code-block:: bash

  */10 * * * * cd path/to/particle/project/ && particle run -c particle.yml

Examples
----------

You can check out some simple examples in the `github repository <https://github.com/abelsonlive/particle/tree/master/examples>`_.


Amazon Machine Image
---------------------

For convenience, I've built an Ubuntu AMI with all dependencies pre-installed.  Due to the large amount of multithreading, ``particle`` seems to work best on a small instance or larger.

`EU West Ireland <https://console.aws.amazon.com/ec2/home?region=eu-west-1#launchAmi=ami-f3113b9a>`_

`US East Virginia <https://console.aws.amazon.com/ec2/home?region=us-east-1#launchAmi=ami-f3113b9a>`_

`US West N California  <https://console.aws.amazon.com/ec2/home?region=us-west-1#launchAmi=ami-f3113b9a>`_

`US West Oregon <https://console.aws.amazon.com/ec2/home?region=us-west-2#launchAmi=ami-f3113b9a>`_

`South America Sao Paulo  <https://console.aws.amazon.com/ec2/home?region=sa-east-1#launchAmi=ami-f3113b9a>`_

`Asia Pacific Singapore <https://console.aws.amazon.com/ec2/home?region=ap-southeast-1#launchAmi=ami-f3113b9a>`_

`Asia Pacific Tokyo <https://console.aws.amazon.com/ec2/home?region=ap-northeast-1#launchAmi=ami-f3113b9a>`_

`Asia Pacific Sydney <https://console.aws.amazon.com/ec2/home?region=ap-southeast-2#launchAmi=ami-f3113b9a>`_


Contents
--------

.. toctree::
   :maxdepth: 2

   install
   config
   web-api
   cli

