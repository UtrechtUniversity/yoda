FROM centos:7
LABEL maintainer="Yoda team <yoda@uu.nl>"

# Network settings
EXPOSE 80
EXPOSE 443

# Application settings
ARG TAG=development
ENV IRODS_VERSION="4.2.11"
ENV YUM_REPO_FILE_LOC "https://packages.irods.org/renci-irods.yum.repo"
ENV YUM_IRODS_REPO_SIGNING_KEY_LOC="https://packages.irods.org/irods-signing-key.asc"
ENV DAVRODS_RPM_URL="https://github.com/UtrechtUniversity/davrods/releases/download/4.2.11_1.5.0/"
ENV DAVRODS_RPM_PACKAGE="davrods-4.2.11_1.5.0-1.rpm"

# Install common tools
# hadolint ignore=DL3033
RUN yum install -y epel-release wget && \
    yum clean all

# Install and configure Apache
# hadolint ignore=DL3033
RUN yum -y install httpd httpd-devel mod_ssl openssl && yum clean all
RUN rm /etc/httpd/conf.d/autoindex.conf /etc/httpd/conf.modules.d/00-lua.conf
COPY httpd.conf /etc/httpd/conf/httpd.conf
COPY ssl.conf /etc/httpd/conf.d/ssl.conf

# Install iRODS components: iCommands and runtime
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
# hadolint ignore=DL3033
RUN yum install -y epel-release wget git && \
    yum clean all && \
    useradd -d /var/lib/irods irods && \
    rpm --import "$YUM_IRODS_REPO_SIGNING_KEY_LOC" && \
    yum update -y ca-certificates && \
    wget -qO - "$YUM_REPO_FILE_LOC" | tee /etc/yum.repos.d/renci-irods.yum.repo && \
    yum -y update && \
    for package in irods-runtime irods-icommands ; \
    do echo "Installing package ${package} and its dependencies ..."; \
       yum -y install "$package-${IRODS_VERSION}"  && yum clean all; \
    done && \
    yum clean all

# Install DavRODS and its dependencies
# hadolint ignore=DL3033
RUN yum -y install boost jansson && yum clean all && \
    mkdir /download && \
    wget -q "$DAVRODS_RPM_URL/$DAVRODS_RPM_PACKAGE" -O "/download/$DAVRODS_RPM_PACKAGE" && \
    rpm -ivh "/download/$DAVRODS_RPM_PACKAGE"

# Copy DavRODS VHost and iRODS configuration files
COPY davrods-vhost.conf /etc/httpd/conf.d/davrods-vhost.conf
COPY davrods-anonymous-vhost.conf /etc/httpd/conf.d/davrods-anonymous-vhost.conf
COPY irods_environment.json /etc/httpd/irods/irods_environment.json

# Copy DavRODS theming files
COPY header.html /etc/httpd/irods/header.html
COPY head.html /etc/httpd/irods/head.html
COPY footer.html /etc/httpd/irods/footer.html

# Initialize
VOLUME [ "/sys/fs/cgroup" ]
COPY davrods_init.sh /var/lib/irods/scripts/davrods_init.sh
RUN chmod 0755 /var/lib/irods/scripts/davrods_init.sh
ENV TAG=${TAG}
CMD exec /var/lib/irods/scripts/davrods_init.sh $TAG
