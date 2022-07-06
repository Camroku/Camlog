# Clog
Camroku's Blog.

## Running
Server configuration requirements:
* Serve `/index.qo` as a CGI script
* Rewrite all URLs ending with `.qo` to `/index.qo`
* Serve `index.qo` as index file
* Deny access for all `.html` files
* Serve everything else as static files

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