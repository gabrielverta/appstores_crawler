# App stores crawler

Crawler for apple and google stores to get ranking of the best apps by category.


## Features

* Paralelism: it uses python 3.5+ async.io lib to get results faster.
* Distributed: you can run it from as many machines you want. 
* Priority to download: as we have an infinity of apps, the most ranked are updated frequently.
* Random range of time to wait between requests to not flood stores.


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