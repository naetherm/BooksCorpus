FROM archlinux/base

MAINTAINER "Markus Näther <naetherm@informatik.uni-freiburg.de>"

# Locale
RUN echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV I_AM_IN_DOCKER_CONTAINER Yes

# Update base system
RUN pacman-key --init && pacman-key --populate \
    && pacman -Syu --noconfirm --noprogressbar pacman \
    && pacman-db-upgrade \
    && pacman -Su --noconfirm --noprogressbar ca-certificates \
    && trust extract-compat \
    && pacman -Syyu --noconfirm --noprogressbar \
    && pacman -Scc --noconfirm

# Install some useful packages to the base system
RUN pacman -Sy --noconfirm --noprogressbar base-devel git sudo zip libglvnd cmake libxml2 boost intel-tbb doxygen graphviz r swig muparser nlopt python-numpydoc python-pip python-scipy python-sphinx python-matplotlib ipython pandoc texlive-latexextra

# Add devel user to build packages
RUN useradd -m -d /home/devel -u 1000 -U -G users,tty -s /bin/bash devel
RUN echo 'devel ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER devel
ENV TERM dumb
ENV MAKEFLAGS "-j8"
RUN git config --global user.email devel@a.b && git config --global user.name devel

