FROM centos:7
LABEL maintainer="Yoda team <yoda@uu.nl>"

# Application settings
ENV IRODS_VERSION "4.2.11"
ENV IRODS_PREP_VERSION "4.2.11.1"
ENV IRODS_INDEX_VERSION "4.2.11.0-1"
ENV IRODS_SUDO_MSVC_VERSION "4.2.11_1.0.0"
ENV IRODS_UU_MSVC_VERSION "0.8.2"
ENV YUM_REPO_FILE_LOC "https://packages.irods.org/renci-irods.yum.repo"
ENV YUM_IRODS_REPO_SIGNING_KEY_LOC="https://packages.irods.org/irods-signing-key.asc"
ENV YODA_RULESET_REPO "https://github.com/UtrechtUniversity/yoda-ruleset.git"
ENV YODA_RULESET_BRANCH "development"

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

# Upload PAM Python library
COPY stage/pam_python.so /tmp/pam_python.so
RUN install -m 0755 -o root -g root /tmp/pam_python.so /usr/lib64/security/pam_python.so

# Install iRODS
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
# hadolint ignore=DL3033
RUN yum install -y epel-release wget git && \
    yum clean all && \
    useradd -d /var/lib/irods irods && \
    rpm --import "$YUM_IRODS_REPO_SIGNING_KEY_LOC" && \
    yum update -y ca-certificates && \
    wget -qO - "$YUM_REPO_FILE_LOC" | tee /etc/yum.repos.d/renci-irods.yum.repo && \
    yum -y update && \
    for package in irods-runtime irods-icommands irods-server irods-database-plugin-postgres; \
    do echo "Installing package ${package} and its dependencies ..."; \
       yum -y install "$package-${IRODS_VERSION}"  && yum clean all; \
    done && \
    for package in irods-rule-engine-plugin-indexing irods-rule-engine-plugin-elasticsearch irods-rule-engine-plugin-document-type; \
    do echo "Installing package ${package} and its dependencies ..."; \
       yum -y install "$package-${IRODS_INDEX_VERSION}"  && yum clean all; \
       done && \
    yum -y install "irods-rule-engine-plugin-python-${IRODS_PREP_VERSION}"  && \
    yum clean all

# Install iRODS microservices for Yoda and their dependencies
# hadolint ignore=DL3033
RUN yum -y install boost-locale jansson libxslt && yum clean all && \
    rpm -ivh "https://github.com/UtrechtUniversity/irods-sudo-microservices/releases/download/${IRODS_SUDO_MSVC_VERSION}/irods-sudo-microservices-${IRODS_SUDO_MSVC_VERSION}-1.rpm" && \
    rpm -ivh "https://github.com/UtrechtUniversity/irods-uu-microservices/releases/download/v${IRODS_UU_MSVC_VERSION}/irods-uu-microservices-${IRODS_VERSION}_${IRODS_UU_MSVC_VERSION}-1.rpm" && \
    chown irods:irods /var/lib/irods

# Remove default iRODS msiExecCMD files
# hadolint ignore=DL3059
RUN for file in irodsServerMonPerf test_execstream.py univMSSInterface.sh.template ; do rm "/var/lib/irods/msiExecCmd_bin/${file}" ; done

# Install iRODS autocompletion
COPY stage/irods_completion.sh /tmp/irods_completion.sh
RUN install -m 0644 -o root -g root /tmp/irods_completion.sh /etc/profile.d/irods_completion.sh

# Set up PAM authentication
# hadolint ignore=DL3033
RUN yum -y install gcc python-pip && \
    yum clean all && \
    pip --no-cache-dir install pysqlcipher3==1.0.4
COPY is-user-external.sh /tmp/is-user-external.sh
COPY external-auth.py /tmp/external-auth.py
RUN install -m 0750 -o root -g irods /tmp/is-user-external.sh /usr/local/bin/is-user-external.sh && \
    install -m 0750 -o root -g irods /tmp/external-auth.py /usr/local/bin/external-auth.py && \
    wget -nv https://github.com/UtrechtUniversity/sqlcipher/releases/download/v4.5.1/sqlcipher-4.5.1-0.el7.x86_64.rpm -O sqlcipher-4.5.1-0.el7.x86_64.rpm && \
    wget -nv https://github.com/UtrechtUniversity/sqlcipher/releases/download/v4.5.1/sqlcipher-devel-4.5.1-0.el7.x86_64.rpm -O sqlcipher-devel-4.5.1-0.el7.x86_64.rpm && \
    rpm -ivh sqlcipher-4.5.1-0.el7.x86_64.rpm && \
    rpm -ivh sqlcipher-devel-4.5.1-0.el7.x86_64.rpm && \
    chmod 04755 /usr/sbin/irodsPamAuthCheck
COPY irods.pam /tmp/irods.pam
RUN install -m 0644 /tmp/irods.pam /etc/pam.d/irods

# Configure iRODS
COPY server_config.json /etc/irods/server_config.json
RUN mkdir /var/lib/irods/.irods
COPY irods_environment.json /var/lib/irods/.irods/irods_environment.json

# Install and configure rulesets
RUN git clone -b ${YODA_RULESET_BRANCH} --single-branch ${YODA_RULESET_REPO} /etc/irods/yoda-ruleset
RUN python -m pip --no-cache-dir install --user pip==20.2.4 && \
    python -m pip --no-cache-dir install --user setuptools==44.1.1 && \ 
    python -m pip --no-cache-dir install --user python-irodsclient==1.1.3 && \
    python -m pip --no-cache-dir install --user -r /etc/irods/yoda-ruleset/requirements.txt
COPY core.py.template /etc/irods/core.py
RUN for script in scheduled-copytovault.sh admin-remove-orphan-vault-if-empty.sh admin-vaultactions.sh \
                  admin-vaultingest.sh enable-indexing.sh disable-indexing.sh  \
                  admin-datarequestactions.sh admin-datarequest-temp-write-permission.sh ; \
    do install -m 0755 /etc/irods/yoda-ruleset/tools/${script} /var/lib/irods/msiExecCmd_bin/${script} ; \
    done && \
    /etc/irods/yoda-ruleset/tools/setup_tokens.sh /etc/irods/yoda-ruleset/accesstokens.db test
COPY stage/run-intake-movetovault.sh /tmp/run-intake-movetovault.sh
COPY job_movetovault.r /var/lib/irods/.irods/job_movetovault.r
COPY job_clearintakelocks.r /var/lib/irods/.irods/job_clearintakelocks.r
RUN install -o irods -g irods -m 0755 /tmp/run-intake-movetovault.sh /var/lib/irods/.irods/run-intake-movetovault.sh
COPY rules_uu.cfg /etc/irods/yoda-ruleset
COPY cronjob-revision-cleanup.sh /tmp/cronjob-revision-cleanup.sh
RUN install -o irods -g irods -m 0755 /tmp/cronjob-revision-cleanup.sh /var/lib/irods/.irods/cronjob-revision-cleanup.sh

VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/sbin/init"]
