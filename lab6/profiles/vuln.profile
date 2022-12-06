include <tunables/global>

profile vuln-httpd-sandbox flags=(attach_disconnected, complain, mediate_deleted) {
  # This 'include' statement imports some very basic permissions from another
  # file, in particular /etc/apparmor.d/abstractions/base. Most AppArmor
  # profiles import abstractions/base somewhere since it's rather convenient.

  include <abstractions/base>

  # The process is allowed to read any file on the file system
  #
  # Note that AppArmor is enforced with the standard Unix DAC permissions. If a
  # user would not traditionally be allowed to read a file, this rule does not
  # override that fact.
  #
  # '**' is a 'glob pattern'. AppArmor profiles support the patterns '*', '**',
  # and '?', which have the following meanings: (see `man apparmor.d`):
  #
  #     *   can substitute for any number of characters, excepting '/'
  #     **  can substitute for any number of characters, including '/'
  #     ?   can substitute for any single character excepting '/'
  #
  # In other words, /** matches any file or directory whose path starts with /
  # (which is *every* file/directory on Linux).

  /** r,

  # We're allowed to execute the /entrypoint.sh script, as well as any program
  # in the directory /usr/local/apache2/.
  #
  # Note that 'ix' means 'inherit execute', i.e. we execute the program and it
  # inherits the same profile we're currently in (the vuln-httpd-sandbox
  # profile). There are some other ways you can specify permissions to execute
  # a program but we won't concern ourselves with that for this lab.

  /entrypoint.sh        ix,
  /usr/local/apache2/** ix,

  # We're allowed to write, link, and lock any file in /usr/local/apache2/logs/*
  #
  # The 'owner' at the front enforces that a user must also be the owner
  # of a file to have these permissions.

  /usr/local/apache2/logs/* wlk,

  # AppArmor is "default deny" so you don't usually need to specify things to
  # deny access to. However, you may occasionally want to explicitly revoke
  # access to something that was granted earlier in the profile.
  #
  # In this case, we previously allowed programs to execute files in
  # /usr/local/apache2/logs/ with the rule
  #
  #     /usr/local/apache2/** ix
  #
  # Since our last rule allowed us to write files to the
  # /usr/local/apache2/logs/ directory, and since there isn't really any reason
  # to allow Apache to execute programs in this directory, we explicitly deny
  # execution access. This ensures that an attacker can't write a file to this
  # directory and then execute it.

  deny /usr/local/apache2/logs/* x,

  # Allow processes to write read/write to /proc/self/fd/*. This allows the
  # program to print messages to stdout and stderr, as well as receive input.
  #
  # See that @{PROC} and @{pid} notation? We're substituting the variables
  # 'PROC' and 'pid' into the rule below, which are defined in
  # /etc/apparmor.d/tunables/proc (and imported at the top of the file when we
  # run #include <tunables/global>).

  owner @{PROC}/@{pid}/fd/* rw,

  #######################################
  # We're not going to concern ourselves too much with the remaining rules.
  # Suffice it to say that these rules allow the container to operate without
  # any issue.
  #
  # Some of the capability rules at the bottom are quite permissive, and
  # we would probably want to be a bit more restrictive in the real world.
  
  deny /sys/firmware/** r,
  deny /sys/kernel/security/** r,

  signal (receive) peer=unconfined,
  signal (receive) peer=dockerd-default,
  signal (send,receive) peer=vuln-httpd-sandbox,
  ptrace (trace,read,tracedby,readby) peer=vuln-httpd-sandbox,

  umount,
  network,
  capability kill,
  capability chown,
  capability dac_override,
  capability setuid,
  capability setgid,
  capability net_bind_service,
}
