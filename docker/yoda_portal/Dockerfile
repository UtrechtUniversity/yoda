FROM centos:7
LABEL maintainer="Yoda team <yoda@uu.nl>"

# Application settings
ENV YODA_PORTAL_REPO "https://github.com/UtrechtUniversity/yoda-portal.git"
ENV YODA_PORTAL_BRANCH "development"

# Network settings
EXPOSE 80
EXPOSE 443

# Install common tools
# hadolint ignore=DL3033
RUN yum install -y epel-release wget git && \
    yum clean all

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

# Yoda Portal
ENV C_INCLUDE_PATH /opt/rh/rh-python38/root/usr/include/python3.8
RUN useradd yodadeployment && \
    mkdir /var/www/yoda && \
    chown yodadeployment:yodadeployment /var/www/yoda && \
    git clone --branch $YODA_PORTAL_BRANCH $YODA_PORTAL_REPO /var/www/yoda
COPY yoda-portal-vhost.conf /etc/httpd/conf.d/yoda-portal-vhost.conf
RUN virtualenv --python /opt/rh/rh-python38/root/bin/python3 /var/www/yoda/venv && \
    /var/www/yoda/venv/bin/pip3 install pip==23.0.1 && \
    /var/www/yoda/venv/bin/pip3 install -r /var/www/yoda/requirements.txt

# Initialize
VOLUME [ "/sys/fs/cgroup" ]
COPY yoda_portal_init.sh /var/lib/irods/scripts/yoda_portal_init.sh
RUN chmod 0755 /var/lib/irods/scripts/yoda_portal_init.sh
CMD ["/var/lib/irods/scripts/yoda_portal_init.sh"]
