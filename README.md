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

## Creating a page
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

### Arguments
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `title` | Set page title | Yes |
| `date` | Set page creation date, as seconds since epoch | Yes |
| `author` | Set author for this page | No |

### `qomar`
If a feature that you need doesn't exist, then you can simply use HTML.

All of the things below can be escaped with `\`.

#### Comments
Everything written between `/*` and `*/` will be ignored by the compiler.
```
/* This is a comment! */
```

#### Code
Everything written between `` ` `` and `` ` `` will be compiled as inline code, and everything written between ```` ``` ```` and ```` ``` ```` will be compiled as block code.
````
`This in inline code!`

```
This is block code!
```
````

#### Paragraphs
Paragraphs can be splitted with two newlines.
```
This is a paragraph.

This is another paragraph.
```

#### Text decoration
The example explains itself.
```
''bold text''

'italic text'

'''italic and bold text'''
```