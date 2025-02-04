FROM ubuntu:24.04
LABEL maintainer="Yoda team <yoda@uu.nl>"
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Application settings
ARG TAG=development
ENV IRODS_VERSION "4.3.4-0~noble"
ENV IRODS_PLUS_VERSION "4.3.4.0-0+4.3.4~noble"
ENV IRODS_MSVC_IRODS_VERSION "4.3.4"
ENV IRODS_SUDO_MSVC_VERSION "1.0.0"
ENV IRODS_UU_MSVC_VERSION "1.2.0"
ENV IRODS_UU_MSVC_VERSION_RELEASE "0"
ENV APT_REPO_CONFIG="deb [arch=amd64] https://packages.irods.org/apt/ noble main"
ENV APT_IRODS_REPO_SIGNING_KEY_LOC="https://packages.irods.org/irods-signing-key.asc"
ENV YODA_RULESET_REPO "https://github.com/UtrechtUniversity/yoda-ruleset.git"
ENV YODA_RULESET_BRANCH="$TAG"
ENV PRE_BUILD_RULESET_DEPENDENCIES "yes"
ENV DEBIAN_FRONTEND="noninteractive"

# Network settings
EXPOSE 1247
EXPOSE 20000-20199

# Suggested base image configuration for systemd, as per
# https://hub.docker.com/_/centos
WORKDIR /lib/systemd/system/sysinit.target.wants/
RUN (for i in *; do [ "$i" = "systemd-tmpfiles-setup.service" ] || rm -f "$i"; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;

# Update packages
RUN apt-get update

# Install common tools
# hadolint ignore=DL3033
RUN apt-get install -y wget git sudo netcat-traditional gcc vim

# Install rsyslog and configure it for logging iRODS messages
# hadolint ignore=DL3033
RUN apt-get install -y rsyslog
COPY stage/irods-log-transform.py /usr/local/sbin/irods-log-transform.py
RUN chmod +x /usr/local/sbin/irods-log-transform.py
COPY rsyslogd-irods.conf /etc/rsyslog.d/40-irods.conf
COPY rsyslog.conf /etc/rsyslog.conf
RUN mkdir /var/lib/irods-log && chown syslog /var/lib/irods-log && chmod 0750 /var/lib/irods-log

# Install Python 3.12
# hadolint ignore=DL3033
RUN apt-get install -y gcc python3 python3-dev python3-pip python3.12-venv python3-virtualenv python3-wheel python3-magic

# Upload PAM Python library
COPY stage/pam_python3.so /tmp/pam_python3.so
RUN mkdir /usr/lib/security
RUN install -m 0755 -o root -g root /tmp/pam_python3.so  /usr/lib/security/pam_python3.so

# Install PostgreSQL 15 for ODBC drivers, checks whether database container is up, as well as troubleshooting
# hadolint ignore=DL3033
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ noble-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list
RUN apt-get update
RUN apt-get -y install postgresql-15 unixodbc unixodbc-dev odbcinst python3-psycopg2 acl
COPY odbc-settings.txt /tmp/odbc-settings.txt
RUN odbcinst -i -d -r < /tmp/odbc-settings.txt

# Install iRODS
# hadolint ignore=DL3033,DL3047
RUN useradd -d /var/lib/irods irods && \
    wget -qO - "$APT_IRODS_REPO_SIGNING_KEY_LOC" | apt-key add - && \
    echo "$APT_REPO_CONFIG" | tee /etc/apt/sources.list.d/irods.list && \
    apt-get update && \
    for package in irods-runtime irods-icommands irods-server irods-database-plugin-postgres; \
    do echo "Installing package ${package} and its dependencies ..."; \
       apt-get -y install "$package=${IRODS_VERSION}" ; \
    done && \
    for package in irods-rule-engine-plugin-python irods-rule-engine-plugin-indexing irods-rule-engine-plugin-elasticsearch; \
    do echo "Installing package ${package} and its dependencies ..."; \
       apt-get -y install "$package=${IRODS_PLUS_VERSION}";  \
       done

# Install iRODS microservices for Yoda
# hadolint ignore=DL3033
RUN apt-get -y install libc++1 libjansson4 && \
    wget -q "https://github.com/UtrechtUniversity/irods-sudo-microservices/releases/download/${IRODS_MSVC_IRODS_VERSION}_${IRODS_SUDO_MSVC_VERSION}/irods-sudo-microservices-${IRODS_MSVC_IRODS_VERSION}-${IRODS_SUDO_MSVC_VERSION}-1.deb" && \
    dpkg -i irods-sudo-microservices-${IRODS_MSVC_IRODS_VERSION}-${IRODS_SUDO_MSVC_VERSION}-1.deb && \
    rm irods-sudo-microservices-${IRODS_MSVC_IRODS_VERSION}-${IRODS_SUDO_MSVC_VERSION}-1.deb && \
    wget -q "https://github.com/UtrechtUniversity/irods-uu-microservices/releases/download/v${IRODS_UU_MSVC_VERSION}/irods-uu-microservices-${IRODS_MSVC_IRODS_VERSION}-${IRODS_UU_MSVC_VERSION}-${IRODS_UU_MSVC_VERSION_RELEASE}.deb" && \
    dpkg -i irods-uu-microservices-${IRODS_MSVC_IRODS_VERSION}-${IRODS_UU_MSVC_VERSION}-${IRODS_UU_MSVC_VERSION_RELEASE}.deb && \
    rm irods-uu-microservices-${IRODS_MSVC_IRODS_VERSION}-${IRODS_UU_MSVC_VERSION}-${IRODS_UU_MSVC_VERSION_RELEASE}.deb && \
    chown irods:irods /var/lib/irods

# Remove default iRODS msiExecCMD files
# hadolint ignore=DL3059
RUN for file in irodsServerMonPerf test_execstream.py univMSSInterface.sh.template ; do rm "/var/lib/irods/msiExecCmd_bin/${file}" ; done

# Install iRODS iCommands autocompletion
COPY stage/irods_completion.sh /tmp/irods_completion.sh
RUN install -m 0644 -o root -g root /tmp/irods_completion.sh /etc/profile.d/irods_completion.sh

# Set up PAM authentication
# hadolint ignore=DL3033
COPY external-auth.py /tmp/external-auth.py
COPY token-auth.py /tmp/token-auth.py
RUN install -m 0750 -o root -g irods /tmp/external-auth.py /usr/local/bin/external-auth.py && \
    install -m 0750 -o root -g irods /tmp/token-auth.py /usr/local/bin/token-auth.py && \
    chmod 04755 /usr/sbin/irodsPamAuthCheck
COPY irods.pam /tmp/irods.pam
COPY oidc.py /tmp/oidc.py
RUN install -m 0644 /tmp/irods.pam /etc/pam.d/irods && \
    install -m 0644 -o irods -g irods /tmp/oidc.py /var/lib/irods/msiExecCmd_bin/oidc.py

# Configure iRODS
COPY server_config.json /etc/irods/server_config.json
RUN mkdir /var/lib/irods/.irods
COPY irods_environment.json /var/lib/irods/.irods/irods_environment.json

# Install and configure rulesets
RUN git clone -b ${YODA_RULESET_BRANCH} ${YODA_RULESET_REPO} /etc/irods/yoda-ruleset
# hadolint ignore=DL3004
RUN sudo -u irods python3 -m pip --no-cache-dir install --user --break-system-packages pip==25.0 && \
    sudo -u irods python3 -m pip --no-cache-dir install --user --break-system-packages -r /etc/irods/yoda-ruleset/requirements.txt && \
    sudo -u irods python3 -m pip install --user --break-system-packages python-irodsclient==3.1.0 && \
    sudo -u irods python3 -m pip install --user --break-system-packages psutil==6.1.0
COPY core.py.template /etc/irods/core.py
COPY core.re.template /etc/irods/core.re
RUN apt-get -y install sqlcipher libsqlcipher1 libsqlcipher-dev
RUN for script in admin-scheduled-copytovault.sh admin-remove-orphan-vault-if-empty.sh admin-vaultactions.sh \
    admin-vaultingest.sh admin-datarequestactions.sh admin-datarequest-temp-write-permission.sh ; \
    do install -m 0755 /etc/irods/yoda-ruleset/tools/admin/${script} /var/lib/irods/msiExecCmd_bin/${script} ; \
    done
RUN for script in enable-indexing.sh disable-indexing.sh; \
    do install -m 0755 /etc/irods/yoda-ruleset/tools/${script} /var/lib/irods/msiExecCmd_bin/${script} ; \
    done && \
    /etc/irods/yoda-ruleset/tools/setup_tokens.sh /etc/irods/yoda-ruleset/accesstokens.db test
COPY cronjob-revision-cleanup.sh /tmp/cronjob-revision-cleanup.sh
RUN install -o irods -g irods -m 0755 /tmp/cronjob-revision-cleanup.sh /var/lib/irods/.irods/cronjob-revision-cleanup.sh
COPY service_account.config /tmp/service_account.config
RUN install -o irods -g irods -m 0644 /tmp/service_account.config /etc/irods/service_account.config

# Install configuration
COPY odbc.ini /var/lib/irods/.odbc.ini
COPY irods_environment.json /var/lib/irods/.irods/irods_environment.json
COPY hosts_config.json /etc/irods/hosts_config.json
COPY host_access_control_config.json /etc/irods/host_access_control_config.json
COPY rules_uu.cfg /etc/irods/yoda-ruleset

# Fix up file ownership iRODS files
RUN chown -R irods:irods /var/lib/irods /etc/irods

# Pre-build ruleset dependencies
RUN test "$PRE_BUILD_RULESET_DEPENDENCIES" = "yes" && git clone --branch "$YODA_RULESET_BRANCH" "$YODA_RULESET_REPO" /var/lib/irods/yoda-ruleset
# hadolint ignore=DL3004
RUN test "$PRE_BUILD_RULESET_DEPENDENCIES" = "yes" && sudo -u irods pip3 install --user --break-system-packages attrs==24.2.0
# hadolint ignore=DL3004
RUN test "$PRE_BUILD_RULESET_DEPENDENCIES" = "yes" && sudo -u irods pip3 install --user --break-system-packages -r /var/lib/irods/yoda-ruleset/requirements.txt

# Create test accounts
# hadolint ignore=SC2016
RUN for user in researcher viewer groupmanager datamanager functionaladmingroup functionaladmincategory functionaladminpriv technicaladmin projectmanager dacmember ; \
    do useradd -m -p '$6$rounds=656000$UYCy5.rN8/Nr5ooZ$.D2DtHyqjMIwQePZ8oGBXkEKTtOeyVPsSK1Kzn/DtIBojPh8ZGxOzVtlrRFMumtgcO7CWzgMAQqxJUORvGiFy0' "$user" ; \
    done

# Make copy of data on volumes that can optionally be bind mounted, so the container init script
# can restore it if needed.
# hadolint ignore=DL3059
RUN cp -Rdp /etc/irods/yoda-ruleset /etc/irods/yoda-ruleset-copy

# Install Docker-specific securecopy script
COPY securecopy.sh /var/lib/irods/securecopy.sh
RUN install -m 0755 -o irods -g irods /var/lib/irods/securecopy.sh /var/lib/irods/msiExecCmd_bin/securecopy.sh

# Install init script
# hadolint ignore=DL3033
COPY irods-icat-init.sh /var/lib/irods/scripts/irods-icat-init.sh
RUN chmod 0755 /var/lib/irods/scripts/irods-icat-init.sh

VOLUME [ "/sys/fs/cgroup" ]
ENV TAG=${TAG}
CMD exec /var/lib/irods/scripts/irods-icat-init.sh $TAG
