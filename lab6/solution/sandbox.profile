# Last Modified: Mon Nov  7 03:15:22 2022
include <tunables/global>

profile sandbox flags=(attach_disconnected, mediate_deleted) {
  include <abstractions/apache2-common>
  include <abstractions/base>
  include <abstractions/nameservice>
  include <abstractions/openssl>
  include <abstractions/php>

  capability dac_override,
  capability setgid,
  capability setuid,

  network,

  signal (receive send) peer=sandbox,
  signal receive peer=dockerd-default,
  signal receive peer=unconfined,

  ptrace (read readby trace tracedby) peer=sandbox,

  # This permission was manually provided in the base profile so that it's
  # still possible to interact with the malicious subdomain at the end of
  # Problem 2.
  /usr/bin/{dash,rm,ls} mrix,

  /var/log/apache2/* w,
  owner /etc/apache2/** r,
  owner /etc/mime.types r,
  owner /run/apache2/* rw,
  owner /usr/sbin/apache2 r,

  owner /var/www/** r,

  # It's also okay to do
  #
  #   owner /var/www/storage/** wk,
  #
  # However, it is *not* okay to allow write access to everything in /var/www,
  # i.e. owner /var/www/** w. The webserver only needs to be able to write
  # files that are in /var/www/storage.
  owner /var/www/storage/framework/** wk,
  owner /var/www/storage/logs/* w,

  # The rule
  #
  #     owner /proc/*/fd/* w,
  #
  # (which is what aa-logprof would suggest) is roughly equivalent.
  owner @{PROC}/@{pid}/fd/* w,

  # Unfortunately necessary -- this is one of the rules that Apache requests
  # according to aa-logprof.
  #
  # In practice this is not really exploitable. Pretty much the only things it
  # allows you to do is list the files/directories that are in the top-level
  # directory / -- it doesn't allow you to read anything in that directory nor
  # in the subdirectories. The write permission is harmless -- the only thing
  # it allows is deleting /, which you can't actually do unless you've also
  # deleted everything under /.
  owner / rw,
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

  /usr/sbin/apache2 mrpx -> sandbox,
  file,

}
