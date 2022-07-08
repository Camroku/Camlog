# Clog
Camroku's Blog.

## Creating a page
Syntax is as follows:
```
title Page title
date Unix timestamp of when it was written
-----
Content
```

Example:
```
title Test page
date 1657226570
-----
Hello!
This is the very first blog page in Clog.
```

You can use HTML in pages. [A markdown-like language](src/qomar.py) is currently being developed.
## Running
Server configuration requirements:
* Serve `/index.qo` as a CGI script
* Rewrite all URLs to `/index.qo`
* Serve `index.qo` as index file
* Deny access for all `.html` files
* Serve all `.js` and `.css` files as static files

Other requirements:
* Latest version of QoLang, which means you have to build it yourself if the latest version isn't a stable version.

After configuring these, you can get your Clog blog to run just like any PHP website.

Example nginx config:
```nginx
# Server configuration for Clog

server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /home/cinar/Clog/src;

        index index.qo;

        server_name localhost;

        location / {
                rewrite (.*) /index.qo last;
        }

        location ~ \.js$|\.css$ {
                try_files $uri @notfound;
        }

        location @notfound {
                rewrite (.*) /index.qo last;
        }

        location ~ \.html$ {
                deny all;
        }

        location = /index.qo {
                include /etc/nginx/fastcgi.conf;
                fastcgi_pass  unix:/var/run/fcgiwrap.socket;
                fastcgi_index index.qo;
        }
}
```