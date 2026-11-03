FROM ubuntu:24.04
LABEL maintainer="Yoda team <yoda@uu.nl>"

# Network settings
EXPOSE 80
EXPOSE 443

# Application settings
ARG TAG=development
ENV IRODS_PACKAGE_VERSION="5.0.2-0~noble"
ENV APT_REPO_CONFIG="deb [arch=amd64] https://packages.irods.org/apt/ noble main"
ENV APT_IRODS_REPO_SIGNING_KEY_LOC="https://packages.irods.org/irods-signing-key.asc"
ENV DAVRODS_APT_URL="https://github.com/UtrechtUniversity/davrods/releases/download/5.0.2_1.5.4"
ENV DAVRODS_APT_PACKAGE="davrods-5.0.2-1.5.4.deb"
ENV DEBIAN_FRONTEND="noninteractive"

# Install packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
                    wget \
                    vim \
                    sudo \
                    netcat-openbsd \
                    gcc \
                    python3 \
                    python3-dev \
                    python3-pip \
                    python3-virtualenv \
                    python3-wheel \
                    python3.12-venv \
                    apache2 \
                    apache2-dev \
                    gnupg \
                    openssl && \
    rm -rf /var/lib/apt/lists/*

# Set up Apache
RUN ln -s /etc/apache2/mods-available/headers.load /etc/apache2/mods-enabled/headers.load
COPY apache2.conf /etc/apache2/apache2.conf
COPY ssl.conf /etc/apache2/mods-available/ssl.conf
RUN ln -s /etc/apache2/mods-available/ssl.load /etc/apache2/mods-enabled/ssl.load && \
    ln -s /etc/apache2/mods-available/dav.load /etc/apache2/mods-enabled/dav.load && \
    ln -s /etc/apache2/mods-available/dav_fs.load /etc/apache2/mods-enabled/dav_fs.load && \
    ln -s /etc/apache2/mods-available/dav_lock.load /etc/apache2/mods-enabled/dav_lock.load && \
    ln -s /etc/apache2/mods-available/davrods.load /etc/apache2/mods-enabled/davrods.load

# Install iRODS components: iCommands and runtime
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
# hadolint ignore=DL3033
RUN useradd -d /var/lib/irods irods && \
    chsh --shell /bin/bash irods && \
    wget -qO - "$APT_IRODS_REPO_SIGNING_KEY_LOC" | apt-key add - && \
    echo "$APT_REPO_CONFIG" | tee /etc/apt/sources.list.d/irods.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
                       irods-runtime=${IRODS_PACKAGE_VERSION} \
                       irods-icommands=${IRODS_PACKAGE_VERSION} \
                       libjansson4 \
                       libboost-all-dev && \
    rm -rf /var/lib/apt/lists/*

# Install DavRODS and its dependencies
RUN mkdir /download && \
    wget -q "$DAVRODS_APT_URL/$DAVRODS_APT_PACKAGE" -O "/download/$DAVRODS_APT_PACKAGE" && \
    dpkg -i "/download/$DAVRODS_APT_PACKAGE"

# Copy DavRODS VHost and iRODS configuration files
COPY davrods-vhost.conf /etc/apache2/sites-available/davrods-vhost.conf
COPY davrods-anonymous-vhost.conf /etc/apache2/sites-available/davrods-anonymous-vhost.conf
RUN ln -s /etc/apache2/sites-available/davrods-vhost.conf /etc/apache2/sites-enabled/davrods-vhost.conf
RUN ln -s /etc/apache2/sites-available/davrods-anonymous-vhost.conf /etc/apache2/sites-enabled/davrods-anonymous-vhost.conf
COPY irods_environment.json /etc/apache2/irods/irods_environment.json

# Copy DavRODS theming files
COPY header.html /etc/apache2/irods/header.html
COPY head.html /etc/apache2/irods/head.html
COPY footer.html /etc/apache2/irods/footer.html

# Copy DavRODS DB initialization script
COPY stage/initialize-davrods-lockdb.py /usr/local/bin/initialize-davrods-lockdb.py

# Initialize
VOLUME [ "/sys/fs/cgroup" ]
COPY davrods_init.sh /var/lib/irods/scripts/davrods_init.sh
RUN chmod 0755 /var/lib/irods/scripts/davrods_init.sh /usr/local/bin/initialize-davrods-lockdb.py
ENV TAG=${TAG}
CMD exec /var/lib/irods/scripts/davrods_init.sh $TAG
