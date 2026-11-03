FROM ubuntu:24.04
LABEL maintainer="Yoda team <yoda@uu.nl>"

# Application settings
ARG TAG=development
ENV YODA_PORTAL_REPO="https://github.com/UtrechtUniversity/yoda-portal.git"
ENV YODA_PORTAL_BRANCH="$TAG"
ENV DEBIAN_FRONTEND="noninteractive"

# Network settings
EXPOSE 80
EXPOSE 443

# Install packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
                    wget \
                    git \
                    vim \
                    sudo \
                    gcc \
                    python3 \
                    python3-dev \
                    python3-pip \
                    python3-virtualenv \
                    python3-wheel \
                    python3.12-venv \
                    virtualenv \
                    apache2 \
                    apache2-dev \
                    openssl \
                    libapache2-mod-wsgi-py3 && \
    rm -rf /var/lib/apt/lists/*
RUN ln -s /etc/apache2/mods-available/headers.load /etc/apache2/mods-enabled/headers.load
COPY apache2.conf /etc/apache2/apache2.conf
COPY ssl.conf /etc/apache2/mods-available/ssl.conf
RUN ln -s /etc/apache2/mods-available/ssl.load /etc/apache2/mods-enabled/ssl.load

# Yoda Portal
RUN useradd yodadeployment && \
    chsh --shell /bin/bash yodadeployment && \
    mkdir /home/yodadeployment && \
    chown yodadeployment:yodadeployment /home/yodadeployment && \
    mkdir /var/www/yoda /var/www/portal-sessions && \
    chown yodadeployment:yodadeployment /var/www/yoda /var/www/portal-sessions && \
    git clone --branch $YODA_PORTAL_BRANCH $YODA_PORTAL_REPO /var/www/yoda && \
    git config --global --add safe.directory /var/www/yoda && \
    chown -R yodadeployment:yodadeployment /var/www/yoda

# Create Yoda Portal config folder
RUN mkdir -p /var/www/yoda/config && \
    chown yodadeployment:yodadeployment /var/www/yoda/config && \
    chmod 0775 /var/www/yoda/config

# Copy Yoda Portal virtual host config for Apache
COPY yoda-portal-vhost.conf /etc/apache2/sites-available/001-yoda-portal-vhost.conf
RUN ln -s /etc/apache2/sites-available/001-yoda-portal-vhost.conf /etc/apache2/sites-enabled/001-yoda-portal-vhost.conf
RUN virtualenv --python /usr/bin/python3 /var/www/yoda/venv && \
    /var/www/yoda/venv/bin/pip3 install --no-cache-dir pip==26.2.2 && \
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
