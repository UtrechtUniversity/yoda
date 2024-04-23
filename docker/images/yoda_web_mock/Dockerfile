FROM ubuntu:20.04
LABEL maintainer="Yoda team <yoda@uu.nl>"

# Application settings
ARG TAG=development
ENV YODA_MOCK_REPO "https://github.com/UtrechtUniversity/yoda-web-mock.git"
ENV YODA_MOCK_BRANCH "$TAG"
ENV DEBIAN_FRONTEND="noninteractive"

# Network settings
EXPOSE 80
EXPOSE 443

# Update packages
RUN apt-get update

# Install common tools (PostgreSQL is needed for psql commands in init script)
# hadolint ignore=DL3033
RUN apt-get install -y wget git netcat gnupg

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

# Install Yoda web mock
RUN useradd yodadeployment && \
    mkdir /home/yodadeployment && \
    chown yodadeployment:yodadeployment /home/yodadeployment && \
    mkdir -p /var/www/webmock/log && \
    chown yodadeployment:yodadeployment /var/www/webmock /var/www/webmock/log && \
    git clone --branch $YODA_MOCK_BRANCH $YODA_MOCK_REPO /var/www/webmock/yoda-web-mock && \
    git config --global --add safe.directory /var/www/webmock/yoda-web-mock
COPY yoda-web-mock-vhost.conf /etc/apache2/sites-available/yoda-web-mock-vhost.conf
RUN ln -s /etc/apache2/sites-available/yoda-web-mock-vhost.conf /etc/apache2/sites-enabled/yoda-web-mock-vhost.conf
RUN virtualenv --python /usr/bin/python3 /var/www/webmock/venv && \
    /var/www/webmock/venv/bin/pip3 install pip==23.0.1 && \
    /var/www/webmock/venv/bin/pip3 install -e /var/www/webmock/yoda-web-mock

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
