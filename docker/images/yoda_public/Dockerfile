FROM centos:7
LABEL maintainer="Yoda team <yoda@uu.nl>"

# Application settings
ENV MOAI_REPO "https://github.com/UtrechtUniversity/yoda-moai.git"
ENV MOAI_BRANCH "development"

# Network settings
EXPOSE 80
EXPOSE 443

# Install common tools
# hadolint ignore=DL3033
RUN yum install -y epel-release wget git nc sudo && \
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

# Install account for MOAI and landing pages
# hadolint ignore=DL3059
RUN useradd yodadeployment -d /var/www/moai

# Install MOAI dependencies
# hadolint ignore=DL3033
RUN yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm && \
    yum -y install sqlite33 sqlite33-devel && yum clean all

## Setup MOAI virtual environment and directory structure
ENV C_INCLUDE_PATH /opt/rh/rh-python38/root/usr/include/python3.8
RUN mkdir -p /var/www/moai /var/www/moai/metadata && \
    git clone --branch "$MOAI_BRANCH" "$MOAI_REPO" /var/www/moai/yoda-moai && \
    chmod 0755 /var/www/moai /var/www/moai/metadata && \
    chown -R yodadeployment:yodadeployment /var/www/moai && \
    virtualenv --python /opt/rh/rh-python38/root/bin/python3 /var/www/moai/yoda-moai/venv && \
    /var/www/moai/yoda-moai/venv/bin/pip3 install pip==23.0.1

## Install PySQLite3 for MOAI
ENV C_INCLUDE_PATH /opt/rh/rh-python38/root/usr/include/python3.8:/usr/sqlite330/include
ENV LIBRARY_PATH /usr/sqlite330/lib
RUN /var/www/moai/yoda-moai/venv/bin/pip3 install pysqlite3==0.5.0

## Install MOAI itself
ENV C_INCLUDE_PATH /opt/rh/rh-python38/root/usr/include/python3.8
RUN /var/www/moai/yoda-moai/venv/bin/pip3 install -e /var/www/moai/yoda-moai

## Configure and initialize MOAI
COPY moai-settings.ini /var/www/moai/settings.ini
COPY moai.wsgi /var/www/moai/moai.wsgi
RUN /var/www/moai/yoda-moai/venv/bin/update_moai --config /var/www/moai/settings.ini yoda_moai

## Install landing page directory structure and static assets
RUN bash -c "mkdir -p /var/www/landingpages/static/{css,img,js}" && \
    chmod -R 0755 /var/www/landingpages && \
    chown -R yodadeployment:yodadeployment /var/www/landingpages
COPY stage/index.html /var/www/landingpages/index.html
COPY stage/bootstrap.min.css /var/www/landingpages/static/css/bootstrap.min.css
COPY stage/uu.css /var/www/landingpages/static/css/uu.css
COPY stage/logo.svg /var/www/landingpages/static/img/logo.svg
COPY stage/logo_footer.svg /var/www/landingpages/static/img/logo_footer.svg

## Configure public web server
COPY yoda-public-vhost.conf /etc/httpd/conf.d/yoda-public-vhost.conf

# Make copy of data on volumes that can optionally be bind mounted, so the container init script
# can restore it if needed.
# hadolint ignore=DL3059
RUN cp -Rdp /var/www/moai/yoda-moai /var/www/moai/yoda-moai-copy

# Initialize
VOLUME [ "/sys/fs/cgroup" ]
COPY yoda_public_init.sh /yoda_public_init.sh
RUN chmod 0755 /yoda_public_init.sh
CMD ["/yoda_public_init.sh"]
