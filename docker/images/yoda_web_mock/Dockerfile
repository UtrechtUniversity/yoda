FROM centos:7
LABEL maintainer="Yoda team <yoda@uu.nl>"

# Application settings
ARG TAG=development
ENV YODA_MOCK_REPO "https://github.com/UtrechtUniversity/yoda-web-mock.git"
ENV YODA_MOCK_BRANCH "$TAG"

# Network settings
EXPOSE 80
EXPOSE 443

# Install common tools
# hadolint ignore=DL3033
RUN yum install -y epel-release wget git nc && \
    yum clean all

# Update packages
RUN yum update -y

# Install Python 3
# hadolint ignore=DL3033
RUN yum -y install centos-release-scl gcc python-virtualenv && \
    yum -y install --enablerepo centos-sclo-rh \
                   rh-python38-python rh-python38-python-devel rh-python38-python-libs \
                   rh-python38-python-pip rh-python38-python-pip-wheel  && yum clean all && \
    ln -s /opt/rh/rh-python38/root/bin/pip3 /usr/local/bin/pip3 && \
    ln -s /opt/rh/rh-python38/root/bin/python3 /usr/local/bin/python33 && \
    /usr/local/bin/pip3 install virtualenv

# Install and configure Apache
# hadolint ignore=DL3033
RUN yum -y install httpd httpd-devel mod_ssl openssl && yum clean all
RUN rm /etc/httpd/conf.d/autoindex.conf /etc/httpd/conf.modules.d/00-lua.conf
COPY httpd.conf /etc/httpd/conf/httpd.conf
COPY ssl.conf /etc/httpd/conf.d/ssl.conf

# Install and configure Apache ModWSGI
RUN yum -y install  --enablerepo centos-sclo-rh rh-python38-python-mod_wsgi && yum clean all
COPY 02-wsgi.conf /etc/httpd/conf.modules.d/02-wsgi.conf
RUN ln -s /opt/rh/rh-python38/root/usr/lib64/python3.8/site-packages/mod_wsgi/server/mod_wsgi-py38.cpython-38-x86_64-linux-gnu.so /usr/lib64/httpd/modules/mod_wsgi.so

# Install Yoda web mock
RUN useradd yodadeployment && \
    mkdir -p /var/www/webmock/log && \
    chown yodadeployment:yodadeployment /var/www/webmock /var/www/webmock/log && \
    git clone --branch $YODA_MOCK_BRANCH $YODA_MOCK_REPO /var/www/webmock/yoda-web-mock
COPY yoda-web-mock-vhost.conf /etc/httpd/conf.d/yoda-web-mock-vhost.conf
RUN virtualenv --python /opt/rh/rh-python38/root/bin/python3 /var/www/webmock/venv && \
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
