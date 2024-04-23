FROM ubuntu:20.04
LABEL maintainer="Yoda team <yoda@uu.nl>"

# Application settings
ARG TAG=development
ENV MOAI_REPO "https://github.com/UtrechtUniversity/yoda-moai.git"
ENV MOAI_BRANCH "$TAG"
ENV DEBIAN_FRONTEND="noninteractive"

# Network settings
EXPOSE 80
EXPOSE 443

# Update packages
RUN apt-get update

# Install common tools
# hadolint ignore=DL3033
RUN apt-get install -y wget git netcat sudo

# Install Python 3
# hadolint ignore=DL3033
RUN apt-get install -y gcc python3 python3-dev python3-pip python3-virtualenv \
                       python3-wheel python3.8-venv virtualenv

# Install and configure Apache
# hadolint ignore=DL3033
RUN apt-get install -y apache2 apache2-dev openssl
RUN ln -s /etc/apache2/mods-available/headers.load /etc/apache2/mods-enabled/headers.load
COPY apache2.conf /etc/apache2/apache2.conf
COPY ssl.conf /etc/apache2/mods-available/ssl.conf
RUN ln -s /etc/apache2/mods-available/ssl.load /etc/apache2/mods-enabled/ssl.load

# Install Apache ModWSGI
RUN apt-get install -y libapache2-mod-wsgi-py3

# Install account for MOAI and landing pages
# hadolint ignore=DL3059
RUN useradd yodadeployment -d /var/www/moai

# Install MOAI dependencies
# hadolint ignore=DL3033
RUN apt-get -y install sqlite3 libsqlite3-dev

## Setup MOAI virtual environment and directory structure
RUN mkdir -p /var/www/moai /var/www/moai/metadata && \
    git clone --branch "$MOAI_BRANCH" "$MOAI_REPO" /var/www/moai/yoda-moai && \
    git config --global --add safe.directory /var/www/moai/yoda-moai && \
    chmod 0755 /var/www/moai /var/www/moai/metadata && \
    chown -R yodadeployment:yodadeployment /var/www/moai && \
    virtualenv --python /usr/bin/python3 /var/www/moai/yoda-moai/venv && \
    /var/www/moai/yoda-moai/venv/bin/pip3 install pip==23.0.1

## Install PySQLite3 for MOAI
ENV C_INCLUDE_PATH /usr/include/python3.8:/usr/include
ENV LIBRARY_PATH /usr/lib/x86_64-linux-gnu
RUN /var/www/moai/yoda-moai/venv/bin/pip3 install pysqlite3==0.5.0

## Install MOAI itself
ENV C_INCLUDE_PATH /usr/include/python3.8
RUN /var/www/moai/yoda-moai/venv/bin/pip3 install -e /var/www/moai/yoda-moai

## Configure and initialize MOAI
COPY moai-settings.ini /var/www/moai/settings.ini
COPY moai.wsgi /var/www/moai/moai.wsgi

## Install landing page directory structure and static assets
RUN bash -c "mkdir -p /var/www/landingpages/static/{css,img,js}" && \
    chmod -R 0755 /var/www/landingpages && \
    chown -R yodadeployment:yodadeployment /var/www/landingpages
COPY stage/index.html /var/www/landingpages/index.html
COPY stage/bootstrap.min.css /var/www/landingpages/static/css/bootstrap.min.css
COPY stage/uu.css /var/www/landingpages/static/css/uu.css
COPY stage/logo.svg /var/www/landingpages/static/img/logo.svg
COPY stage/logo_footer.svg /var/www/landingpages/static/img/logo_footer.svg
COPY stage/leaflet-1.5.1.css /var/www/landingpages/static/css/leaflet-1.5.1.css
COPY stage/leaflet-1.5.1.js /var/www/landingpages/static/js/leaflet-1.5.1.js

RUN cp -Rdp /var/www/landingpages /var/www/landingpages-copy

## Configure public web server
COPY yoda-public-vhost.conf /etc/apache2/sites-available/yoda-public-vhost.conf
RUN ln -s /etc/apache2/sites-available/yoda-public-vhost.conf /etc/apache2/sites-enabled/yoda-public-vhost.conf

# Make copy of data on volumes that can optionally be bind mounted, so the container init script
# can restore it if needed.
# hadolint ignore=DL3059
RUN cp -Rdp /var/www/moai/yoda-moai /var/www/moai/yoda-moai-copy

# Initialize
VOLUME [ "/sys/fs/cgroup" ]
COPY yoda_public_init.sh /yoda_public_init.sh
RUN chmod 0755 /yoda_public_init.sh
ENV TAG=${TAG}
CMD exec /yoda_public_init.sh $TAG
