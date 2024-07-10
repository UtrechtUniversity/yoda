FROM ubuntu:20.04
LABEL maintainer="Yoda team <yoda@uu.nl>"

# Application settings
ARG TAG=development
ENV YODA_PORTAL_REPO "https://github.com/UtrechtUniversity/yoda-portal.git"
ENV YODA_PORTAL_BRANCH="$TAG"
ENV DEBIAN_FRONTEND="noninteractive"

# Network settings
EXPOSE 80
EXPOSE 443

# Update packages
RUN apt-get update

# Install common tools
# hadolint ignore=DL3033
RUN apt-get install -y wget git vim

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

# Yoda Portal
RUN useradd yodadeployment && \
    mkdir /home/yodadeployment && \
    chown yodadeployment:yodadeployment /home/yodadeployment && \
    mkdir /var/www/yoda && \
    chown yodadeployment:yodadeployment /var/www/yoda && \
    git clone --branch $YODA_PORTAL_BRANCH $YODA_PORTAL_REPO /var/www/yoda && \
    git config --global --add safe.directory /var/www/yoda
COPY yoda-portal-vhost.conf /etc/apache2/sites-available/001-yoda-portal-vhost.conf
RUN ln -s /etc/apache2/sites-available/001-yoda-portal-vhost.conf /etc/apache2/sites-enabled/001-yoda-portal-vhost.conf
RUN virtualenv --python /usr/bin/python3 /var/www/yoda/venv && \
    /var/www/yoda/venv/bin/pip3 install --no-cache-dir pip==23.0.1 && \
    /var/www/yoda/venv/bin/pip3 install --no-cache-dir -r /var/www/yoda/requirements.txt

# Make copy of data on volumes that can optionally be bind mounted, so the container init script
# can restore it if needed.
RUN cp -Rdp /var/www/yoda /var/www/yoda-copy

# Initialize
VOLUME [ "/sys/fs/cgroup" ]
COPY yoda_portal_init.sh /var/lib/irods/scripts/yoda_portal_init.sh
RUN chmod 0755 /var/lib/irods/scripts/yoda_portal_init.sh
ENV TAG=${TAG}
CMD exec /var/lib/irods/scripts/yoda_portal_init.sh $TAG
