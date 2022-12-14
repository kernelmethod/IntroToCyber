include <tunables/global>

profile ticktock-web flags=(attach_disconnected, mediate_deleted, complain) {
  include <abstractions/base>

  # TODO: your rules here!
}

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
  include <abstractions/base>

  # Transition into the `sandbox` profile upon executing Gunicorn
  /usr/local/bin/gunicorn mrpx -> ticktock-web,

  signal (receive) peer=unconfined,
  signal (receive) peer=dockerd-default,
  signal (send,receive) peer=vuln-httpd-sandbox,
  ptrace (trace,read,tracedby,readby) peer=vuln-httpd-sandbox,

  umount,
  network,
  capability,
  file,

  deny @{PROC}/* w,
  deny @{PROC}/sys/** w,
  deny @{PROC}/sysrq-trigger rwklx,
  deny @{PROC}/kcore rwklx,

  deny mount,

  deny /sys/** wkl,
  deny /sys/firmware/** rx,
  deny /sys/kernel/security/** rx,

  signal (receive) peer=unconfined,
  signal (receive) peer=dockerd-default,
  signal (send,receive) peer=sandbox-init,
  ptrace (trace,read,tracedby,readby) peer=sandbox-init,
}
