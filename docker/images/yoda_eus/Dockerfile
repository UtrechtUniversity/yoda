FROM ubuntu:20.04
LABEL maintainer="Yoda team <yoda@uu.nl>"

# Application settings
ARG TAG=development
ENV YODA_EUS_REPO "https://github.com/UtrechtUniversity/yoda-external-user-service.git"
ENV YODA_EUS_BRANCH "$TAG"
ENV YODA_PORTAL_REPO "https://github.com/UtrechtUniversity/yoda-portal.git"
ENV YODA_PORTAL_BRANCH "$TAG"
ENV DEBIAN_FRONTEND="noninteractive"
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Network settings
EXPOSE 80
EXPOSE 443

# Update packages
RUN apt-get update

# Install common tools (PostgreSQL is needed for psql commands in init script)
# hadolint ignore=DL3033
RUN apt-get install -y wget git netcat gnupg vim

# Install PostgreSQL 15 for checks whether database container is up, as well as troubleshooting
# hadolint ignore=DL3033
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ focal-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list
RUN apt-get update
RUN apt-get -y install postgresql-15 python3-psycopg2 acl

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

# Yoda EUS (and portal for theming data)
RUN useradd yodadeployment && \
    mkdir /home/yodadeployment && \
    chown yodadeployment:yodadeployment /home/yodadeployment && \
    mkdir /var/www/yoda /var/www/extuser && \
    chown yodadeployment:yodadeployment /var/www/yoda /var/www/extuser && \
    git clone --branch $YODA_EUS_BRANCH $YODA_EUS_REPO /var/www/extuser/yoda-external-user-service && \
    git clone --branch $YODA_PORTAL_BRANCH $YODA_PORTAL_REPO /var/www/yoda && \
    git config --global --add safe.directory /var/www/yoda && \
    git config --global --add safe.directory /var/www/yoda-external-user-service
COPY yoda-external-user-service-vhost.conf /etc/apache2/sites-available/003-yoda-eus-vhost.conf
RUN ln -s /etc/apache2/sites-available/003-yoda-eus-vhost.conf /etc/apache2/sites-enabled/003-yoda-eus-vhost.conf
RUN virtualenv --python /usr/bin/python3  /var/www/extuser/yoda-external-user-service/venv && \
    /var/www/extuser/yoda-external-user-service/venv/bin/pip3 install --no-cache-dir pip==23.0.1 && \
    /var/www/extuser/yoda-external-user-service/venv/bin/pip3 install --no-cache-dir /var/www/extuser/yoda-external-user-service

# Make copy of data on volumes that can optionally be bind mounted, so the container init script
# can restore it if needed.
# hadolint ignore=DL3059
RUN cp -Rdp /var/www/yoda /var/www/yoda-copy
# hadolint ignore=DL3059
RUN cp -Rdp /var/www/extuser /var/www/extuser-copy

# Initialize
VOLUME [ "/sys/fs/cgroup" ]
COPY yoda_eus_init.sh /var/lib/irods/scripts/yoda_eus_init.sh
RUN chmod 0755 /var/lib/irods/scripts/yoda_eus_init.sh
ENV TAG=${TAG}
CMD exec /var/lib/irods/scripts/yoda_eus_init.sh $TAG
