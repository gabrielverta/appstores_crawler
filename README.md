# App stores crawler

Crawler for apple and google stores to get ranking of the best apps by category.


## Features

* Concurrent: it uses python 3.5+ async.io lib to get results faster
* Distributed: you can run the crawler from as many machines you want using a centralized db
* Priority to download: as the stores have an infinity of apps, the most ranked apps are updated frequently. We don't need to download all the apps before start the updates.
* Configurable random range of time to wait between requests to not flood app stores


## How does it work?


### Microservices

There are 2 microservices:

1. **urldb**: handles the queue of which urls must be downloaded, and saves new ones to the queue
2. **appsdb**: handles the apps creation and queries

### Crawler

Crawls the categories of the app stores, and than ask for *urldb* which URLs are next in queue to be crawled. 
It also send new apps URLs to the *urldb* to be handled

## How to run it?

...