FROM ubuntu:24.04
LABEL maintainer="Yoda team <yoda@uu.nl>"

# Network settings
EXPOSE 80
EXPOSE 443

# Application settings
ARG TAG=development
ENV IRODS_PACKAGE_VERSION="4.3.4-0~noble"
ENV APT_REPO_CONFIG="deb [arch=amd64] https://packages.irods.org/apt/ noble main"
ENV APT_IRODS_REPO_SIGNING_KEY_LOC="https://packages.irods.org/irods-signing-key.asc"
ENV DAVRODS_APT_URL="https://github.com/UtrechtUniversity/davrods/releases/download/4.3.4_1.5.1"
ENV DAVRODS_APT_PACKAGE="davrods-4.3.4-1.5.1.deb"
ENV DEBIAN_FRONTEND="noninteractive"

# Update packages
RUN apt-get update

# Install common tools
# hadolint ignore=DL3033
RUN apt-get install -y wget vim sudo

# Install Python 3
# hadolint ignore=DL3033
RUN apt-get install -y gcc python3 python3-dev python3-pip python3-virtualenv \
                       python3-wheel python3.12-venv

# Install and configure Apache
# hadolint ignore=DL3033
RUN apt-get install -y apache2 apache2-dev openssl
RUN ln -s /etc/apache2/mods-available/headers.load /etc/apache2/mods-enabled/headers.load
COPY apache2.conf /etc/apache2/apache2.conf
COPY ssl.conf /etc/apache2/mods-available/ssl.conf
RUN ln -s /etc/apache2/mods-available/ssl.load /etc/apache2/mods-enabled/ssl.load
RUN ln -s /etc/apache2/mods-available/dav.load /etc/apache2/mods-enabled/dav.load
RUN ln -s /etc/apache2/mods-available/dav_fs.load /etc/apache2/mods-enabled/dav_fs.load
RUN ln -s /etc/apache2/mods-available/dav_lock.load /etc/apache2/mods-enabled/dav_lock.load
RUN ln -s /etc/apache2/mods-available/davrods.load /etc/apache2/mods-enabled/davrods.load

# Install iRODS components: iCommands and runtime
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
# hadolint ignore=DL3033
RUN useradd -d /var/lib/irods irods && \
    chsh --shell /bin/bash irods && \
    wget -qO - "$APT_IRODS_REPO_SIGNING_KEY_LOC" | apt-key add - && \
    echo "$APT_REPO_CONFIG" | tee /etc/apt/sources.list.d/irods.list && \
    apt-get update && \
    apt-cache policy irods-runtime && \
    apt-cache policy irods-icommands && \
    apt-get -y install irods-runtime=${IRODS_PACKAGE_VERSION} irods-icommands=${IRODS_PACKAGE_VERSION}

# Install DavRODS and its dependencies
# hadolint ignore=DL3033
RUN apt-get -y install libboost-all-dev libjansson4 && \
    mkdir /download && \
    wget -q "$DAVRODS_APT_URL/$DAVRODS_APT_PACKAGE" -O "/download/$DAVRODS_APT_PACKAGE" && \
    dpkg -i "/download/$DAVRODS_APT_PACKAGE"

# Copy DavRODS VHost and iRODS configuration files
COPY davrods-vhost.conf /etc/apache2/stes-available/davrods-vhost.conf
COPY davrods-anonymous-vhost.conf /etc/apache2/sites-available/davrods-anonymous-vhost.conf
RUN ln -s /etc/apache2/sites-available/davrods-vhost.conf /etc/apache2/sites-enabled/davrods-vhost.conf
RUN ln -s /etc/apache2/sites-available/davrods-anonymous-vhost.conf /etc/apache2/sites-enabled/davrods-anonymous-vhost.conf
COPY irods_environment.json /etc/apache2/irods/irods_environment.json

# Copy DavRODS theming files
COPY header.html /etc/apache2/irods/header.html
COPY head.html /etc/apache2/irods/head.html
COPY footer.html /etc/apache2/irods/footer.html

# Initialize
VOLUME [ "/sys/fs/cgroup" ]
COPY davrods_init.sh /var/lib/irods/scripts/davrods_init.sh
RUN chmod 0755 /var/lib/irods/scripts/davrods_init.sh
ENV TAG=${TAG}
CMD exec /var/lib/irods/scripts/davrods_init.sh $TAG
