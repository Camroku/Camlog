# Clog
Camroku's Blog.

## Running
Server configuration requirements:
* Serve `/index.qo` as a CGI script
* Rewrite all URLs to `/index.qo`
* Serve `index.qo` as index file
* Deny access for all `.html` files
* Serve all `.js` and `.css` files as static files

Other requirements:
* Latest version of QoLang, built with `IMPORTS=sqlite3`.

After configuring these, you can get your Clog blog to run just like any PHP website. Don't forget to create `src/authors` and `src/pages` directories.

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

## Creating a page
You should create a file under `src/pages/` with `.qm` extension.

Syntax is as follows:
```
arg value
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

You can use HTML in pages. [A markdown-like language](#qomar) is currently being developed.

Import note: The first line should be a short description without anything that would look weird as plain text, because the first line is used as the description for the RSS feed.

### Arguments
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `title` | Set page title | Yes |
| `date` | Set page creation date, as seconds since epoch | Yes |
| `author` | Set author for this page | No |
| `tag` | Add a tag for this page | No |

## Creating an author page
You should create a file under `src/authors/` with `.qm` extension.

Example:
```
realname Çınar Yılmaz
pfp https://avatars.githubusercontent.com/u/79412062
link My Website | https://camroku.tech/
link QoLang | https://qolang.camroku.tech/
-----
Hello! I\'m Arnolxu.
```

### Arguments
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `realname` | Author's IRL name | No |
| `pfp` | Link to the author's profile photo | No |
| `link` | A link (Syntax: `link Text \| Link`) | No |

## `qomar`
A markup language, developed for Clog. See [tutorial](src/pages/qomar_tutor.qm).
