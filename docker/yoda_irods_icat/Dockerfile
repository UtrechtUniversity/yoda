FROM centos:7
LABEL maintainer="Yoda team <yoda@uu.nl>"

# Application settings
ENV IRODS_VERSION "4.2.11"
ENV PREP_VERSION "4.2.11.1"
ENV IRODS_SUDO_MSVC_VERSION "4.2.11_1.0.0"
ENV IRODS_UU_MSVC_VERSION "0.8.2"
ENV YUM_REPO_FILE_LOC "https://packages.irods.org/renci-irods.yum.repo"
ENV YUM_IRODS_REPO_SIGNING_KEY_LOC="https://packages.irods.org/irods-signing-key.asc"

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

# Install iRODS
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
# hadolint ignore=DL3033
RUN yum install -y epel-release wget  && yum clean all
RUN useradd -d /var/lib/irods irods
RUN rpm --import "$YUM_IRODS_REPO_SIGNING_KEY_LOC"
RUN yum update -y ca-certificates
RUN wget -qO - "$YUM_REPO_FILE_LOC" | tee /etc/yum.repos.d/renci-irods.yum.repo
RUN yum -y update
RUN for package in irods-runtime irods-icommands irods-server irods-database-plugin-postgres; \
    do echo "Installing package ${package} and its dependencies ..."; \
       yum -y install "$package-${IRODS_VERSION}"  && yum clean all; \
    done
RUN yum -y install "irods-rule-engine-plugin-python-${PREP_VERSION}"  && yum clean all

# Install iRODS microservices for Yoda and their dependencies
# hadolint ignore=DL3033
RUN yum -y install boost-locale jansson libxslt && yum clean all
RUN rpm -ivh "https://github.com/UtrechtUniversity/irods-sudo-microservices/releases/download/${IRODS_SUDO_MSVC_VERSION}/irods-sudo-microservices-${IRODS_SUDO_MSVC_VERSION}-1.rpm"
RUN rpm -ivh "https://github.com/UtrechtUniversity/irods-uu-microservices/releases/download/v${IRODS_UU_MSVC_VERSION}/irods-uu-microservices-${IRODS_VERSION}_${IRODS_UU_MSVC_VERSION}-1.rpm"
RUN chown irods:irods /var/lib/irods

VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/sbin/init"]
