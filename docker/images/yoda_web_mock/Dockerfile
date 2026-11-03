FROM ubuntu:24.04
LABEL maintainer="Yoda team <yoda@uu.nl>"

# Application settings
ARG TAG=development
ENV YODA_MOCK_REPO="https://github.com/UtrechtUniversity/yoda-web-mock.git"
ENV YODA_MOCK_BRANCH="$TAG"
ENV DEBIAN_FRONTEND="noninteractive"

# Network settings
EXPOSE 80
EXPOSE 443

# Install packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
                    wget \
                    git \
                    netcat-traditional \
                    gnupg \
                    vim \
                    sudo \
                    gcc  \
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

# Install and configure Apache
RUN ln -s /etc/apache2/mods-available/headers.load /etc/apache2/mods-enabled/headers.load
COPY apache2.conf /etc/apache2/apache2.conf
COPY ssl.conf /etc/apache2/mods-available/ssl.conf
RUN ln -s /etc/apache2/mods-available/ssl.load /etc/apache2/mods-enabled/ssl.load

# Install Yoda web mock
RUN useradd yodadeployment && \
    chsh --shell /bin/bash yodadeployment && \
    mkdir /home/yodadeployment && \
    chown yodadeployment:yodadeployment /home/yodadeployment && \
    mkdir -p /var/www/webmock/log && \
    chown yodadeployment:yodadeployment /var/www/webmock /var/www/webmock/log && \
    mkdir -p /var/www/webmock/sram && \
    chown yodadeployment:yodadeployment /var/www/webmock /var/www/webmock/sram && \
    git clone --branch $YODA_MOCK_BRANCH $YODA_MOCK_REPO /var/www/webmock/yoda-web-mock && \
    git config --global --add safe.directory /var/www/webmock/yoda-web-mock
COPY --chown=yodadeployment:yodadeployment sram_mock.json /var/www/webmock/sram/sram_mock.json
COPY yoda-web-mock-vhost.conf /etc/apache2/sites-available/yoda-web-mock-vhost.conf
RUN ln -s /etc/apache2/sites-available/yoda-web-mock-vhost.conf /etc/apache2/sites-enabled/yoda-web-mock-vhost.conf
RUN virtualenv --python /usr/bin/python3 /var/www/webmock/venv && \
    /var/www/webmock/venv/bin/pip3 install --no-cache-dir virtualenv==20.28.0 && \
    /var/www/webmock/venv/bin/python3 -m virtualenv /var/www/webmock/venv && \
    /var/www/webmock/venv/bin/pip3 install --no-cache-dir pip==26.2.2 && \
    /var/www/webmock/venv/bin/pip3 install --no-cache-dir -e /var/www/webmock/yoda-web-mock

# Make copy of data on volumes that can optionally be bind mounted, so the container init script
# can restore it if needed.
# hadolint ignore=DL3059
RUN cp -Rdp /var/www/webmock/yoda-web-mock /var/www/webmock/yoda-web-mock-copy

# Initialize
VOLUME [ "/sys/fs/cgroup" ]
COPY yoda_web_mock_init.sh /yoda_web_mock_init.sh
RUN chmod 0755 /yoda_web_mock_init.sh
ENV TAG=${TAG}
CMD exec /yoda_web_mock_init.sh $TAG
