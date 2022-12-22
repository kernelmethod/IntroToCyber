# Last Modified: Sun Dec 18 18:50:48 2022
#include <tunables/global>

#######################################################
#
# You may ignore the following ticktock-init profile. This AppArmor profile
# gets used by the webserver container before it transitions into the
# ticktock-web profile.
#
# Based on the default Podman profile:
#
# https://github.com/containers/podman/blob/main/vendor/github.com/containers/common/pkg/apparmor/apparmor_linux_template.go


profile ticktock-init flags=(attach_disconnected, mediate_deleted) {
  #include <abstractions/base>

  capability,

  network,

  deny mount,

  umount,

  signal (receive send) peer=sandbox-init,
  signal (receive send) peer=vuln-httpd-sandbox,
  signal receive peer=dockerd-default,
  signal receive peer=dockerd-default,
  signal receive peer=unconfined,
  signal receive peer=unconfined,

  ptrace (read readby trace tracedby) peer=sandbox-init,
  ptrace (read readby trace tracedby) peer=vuln-httpd-sandbox,

  deny /sys/** wlk,
  deny /sys/firmware/** rx,
  deny /sys/kernel/security/** rx,
  deny @{PROC}/* w,
  deny @{PROC}/kcore rwlkx,
  deny @{PROC}/sys/** w,
  deny @{PROC}/sysrq-trigger rwlkx,

  /usr/local/bin/gunicorn mrpx -> ticktock-web,
  file,

}
profile ticktock-web flags=(attach_disconnected, mediate_deleted, complain) {
  #include <abstractions/base>
  #include <abstractions/nameservice>
  #include <abstractions/openssl>
  #include <abstractions/user-tmp>

  /bin/busybox r,
  /etc/gunicorn/* r,
  /sbin/ldconfig mrix,

  /usr/local/bin/ r,
  /usr/local/bin/gunicorn r,
  /usr/local/bin/python3.10 r,

  /usr/local/lib/libpython*so* mr,
  /usr/local/lib/python3.10/{,**} mr,

  /usr/share/misc/magic.mgc r,

  owner /proc/*/fd/ r,
  owner /var/cache/pycache/** rw,
  owner /var/log/ticktock/* w,
  owner /var/opt/ticktock/{,**} r,

}
