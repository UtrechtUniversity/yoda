FROM centos:7
MAINTAINER Yoda Team <yoda@uu.nl>

# Application settings
ENV IRODS_VERSION "4.2.11"
ENV PREP_VERSION "4.2.11.1"
ENV YUM_REPO_FILE_LOC "https://packages.irods.org/renci-irods.yum.repo"
ENV YUM_IRODS_REPO_SIGNING_KEY_LOC="https://packages.irods.org/irods-signing-key.asc"

# Network settings
EXPOSE 1247
EXPOSE 20000-20199

# Suggested base image configuration for systemd, as per
# https://hub.docker.com/_/centos
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;

# Install iRODS
RUN yum install -y epel-release wget
RUN rpm --import "$YUM_IRODS_REPO_SIGNING_KEY_LOC"
RUN yum update -y ca-certificates
RUN wget -qO - "$YUM_REPO_FILE_LOC" | tee /etc/yum.repos.d/renci-irods.yum.repo
RUN yum -y update
RUN for package in irods-runtime irods-icommands irods-server irods-database-plugin-postgres; \
    do echo "Installing package ${package} and its dependencies ..."; \
       yum -y install "$package-${IRODS_VERSION}" ; \
    done
RUN yum -y install "irods-rule-engine-plugin-python-${PREP_VERSION}"

VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/sbin/init"]
