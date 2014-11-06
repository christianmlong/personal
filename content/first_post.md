Title: Pelican 
Category: Python
Tags: pelican, blog
Slug: first-post
Author: Christian Long
Summary: First post to my new Pelican-Powered blog

With a bit of wrangling, I got Pelican working to manage my blog. [Pelican](http://blog.getpelican.com/) is a static site generator written in Python. It can handle reStructuredText, Markdown, or AsciiDoc formats.

The next question is, what theme to use? The [Pelican theme gallery](http://pelican-themes-gallery.place.org/) is helpful here. I debated between these themes:

* [Irfan](http://pelican-themes-gallery.place.org/irfan/)
* [Tuxlite TBS](http://pelican-themes-gallery.place.org/tuxlite_tbs/)
* [Pelican Mockingbird](http://pelican-themes-gallery.place.org/pelican-mockingbird/)
* [Built Texts](http://pelican-themes-gallery.place.org/built-texts/)

For now, I'm using [Built Texts](http://pelican-themes-gallery.place.org/built-texts/). It's as easy as setting 

```THEME = /path/to/built-texts``` 

in your pelicanconf.py. 

Also, make sure that you set 

```SITEURL = ''```

in pelicanconf.py. Otherwise, your local preview site will try to load resoureces (css, etc.) from the url of your published site. 

