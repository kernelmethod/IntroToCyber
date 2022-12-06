include <tunables/global>

profile sandbox flags=(attach_disconnected, complain, mediate_deleted) {
  include <abstractions/base>

  ## TODO: your rules here!

  #######################################################

  # Do *not* delete this rule. The web server doesn't actually need to run rm
  # or ls for any reason, but these will be useful for seeing what you are and
  # aren't able to do at the end of Problem 2.
  /usr/bin/{rm,ls,dash} mrix,

  # Allow network access
  #
  # This permission may get brought in by one of your other rules but
  # aa-logprof doesn't really seem to recognize when this permission is required,
  # at least not in a Docker container.
  network,

  # The following rules make it possible for the sandboxed process to receive
  # signals from other processes, as well as send signals to its own processes.
  # This is necessary in order to run httpd, but it's also required for things
  # like `docker compose down` and `docker kill`

  signal (receive) peer=unconfined,
  signal (receive) peer=dockerd-default,
  signal (send,receive) peer=sandbox,
  ptrace (trace,read,tracedby,readby) peer=sandbox,
}

#######################################################
#
# Ignore this profile! You should not need to use it. It's here to make your
# lives a bit easier.
#
# This is the AppArmor profile that the container starts in before it runs the
# `sandbox` profile. This is very permissive; the main point of it is that to
# transition into the `sandbox` profile once `apache2` is executed.
#
# Based on the default Podman profile:
#
# https://github.com/containers/podman/blob/main/vendor/github.com/containers/common/pkg/apparmor/apparmor_linux_template.go

profile sandbox-init flags=(attach_disconnected, mediate_deleted) {
  include <abstractions/base>

  # Transition into the `sandbox` profile upon executing httpd
  /usr/sbin/apache2 mrpx -> sandbox,

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
