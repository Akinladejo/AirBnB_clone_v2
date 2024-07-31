$nginx_conf = '
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}'

package { 'nginx':
  ensure   => 'present',
  provider => 'apt',
}

file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/releases/test', '/data/web_static/shared', '/var/www', '/var/www/html']:
  ensure => 'directory',
}

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Holberton School Puppet\n",
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

file { ['/var/www/html/index.html', '/var/www/html/404.html']:
  ensure  => 'present',
  content => "Holberton School Nginx\n",
}

file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf,
}

service { 'nginx':
  ensure    => 'running',
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
