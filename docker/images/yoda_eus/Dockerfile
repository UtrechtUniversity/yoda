FROM centos:7
LABEL maintainer="Yoda team <yoda@uu.nl>"

# Application settings
ARG TAG=development
ENV YODA_EUS_REPO "https://github.com/UtrechtUniversity/yoda-external-user-service.git"
ENV YODA_EUS_BRANCH "$TAG"
ENV YODA_PORTAL_REPO "https://github.com/UtrechtUniversity/yoda-portal.git"
ENV YODA_PORTAL_BRANCH "$TAG"

# Network settings
EXPOSE 80
EXPOSE 443

# Install common tools (PostgreSQL is needed for psql commands in init script)
# hadolint ignore=DL3033
RUN yum install -y epel-release wget git nc && \
    yum clean all

# Update packages
RUN yum update -y

# Install PostgreSQL 15 for checks whether database container is up, as well as troubleshooting
# hadolint ignore=DL3033
RUN yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm && \
    yum -y install libzstd-devel postgresql15 && \
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

# Yoda EUS (and portal for theming data)
ENV C_INCLUDE_PATH /opt/rh/rh-python38/root/usr/include/python3.8
RUN useradd yodadeployment && \
    mkdir /var/www/yoda /var/www/extuser && \
    chown yodadeployment:yodadeployment /var/www/yoda /var/www/extuser && \
    git clone --branch $YODA_EUS_BRANCH $YODA_EUS_REPO /var/www/extuser/yoda-external-user-service && \
    git clone --branch $YODA_PORTAL_BRANCH $YODA_PORTAL_REPO /var/www/yoda
COPY yoda-external-user-service-vhost.conf /etc/httpd/conf.d/yoda-external-user-service-vhost.conf
RUN virtualenv --python /opt/rh/rh-python38/root/bin/python3 /var/www/extuser/yoda-external-user-service/venv && \
    /var/www/extuser/yoda-external-user-service/venv/bin/pip3 install pip==23.0.1 && \
    /var/www/extuser/yoda-external-user-service/venv/bin/pip3 install /var/www/extuser/yoda-external-user-service

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
