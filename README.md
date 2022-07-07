# Clog
Camroku's Blog.

## Creating a page
Syntax is as follows:
```
Page title
Unix timestamp of when it was written
-----
Content
```

Example:
```
Test page
1657226570
-----
Hello!
This is the very first blog page in Clog.
```

## Running
Server configuration requirements:
* Serve `/index.qo` as a CGI script
* Rewrite all URLs ending with `.qo` to `/index.qo`
* Serve `index.qo` as index file
* Deny access for all `.html` files
* Serve everything else as static files

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
                try_files $uri $uri/ =404;
        }

        location ~ \.qo$ {
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