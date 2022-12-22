# Final exam -- solutions

- [Problem 1: Cryptography](#problem-1-cryptography)
- [Problem 2: Networking](#problem-2-networking)
- [Problem 3: Access control](#problem-3-access-control)
- [Problem 4: Detection](#problem-4-detection)

## Problem 1: Cryptography

All of the problems on the final were challenging in their own right, but this
one was (in my opinion) the most difficult.

Let's look at that code snippet again:

```python
import os
from base64 import b64encode
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

ikm = os.environ["CRYPTO_IKM"].encode("utf-8")
if len(ikm) < 32:
    raise RuntimeError("Input key material must be at least 32 bytes")

hkdf = HKDF(SHA256(), length=32, salt=b"", info=b"Encrypt")
CHACHA_KEY: bytes = hkdf.derive(ikm)

hkdf = HKDF(SHA256(), length=32, salt=b"", info=b"GenerateNonce")
NONCE_KEY: bytes = hkdf.derive(ikm)


def encrypt(filename: str, contents: bytes):
    cipher = ChaCha20Poly1305(CHACHA_KEY)
    filename_as_bytes = filename.encode("utf-8")
    hkdf = HKDF(SHA256(), length=12, salt=b"", info=filename_as_bytes)
    nonce = hkdf.derive(NONCE_KEY)
    ciphertext = cipher.encrypt(nonce, contents, filename_as_bytes)

    # Poly1305 tag is stored in the last 16 bytes of the
    # ChaCha20Poly1305 output
    ct, tag = ciphertext[:-16], ciphertext[-16:]
    return {"ciphertext": b64encode(ct), "tag": b64encode(tag), "filename": filename}
```

The important bit here is the `encrypt` function. Let's look at what it does,
going roughly line-by-line (we'll discuss the lines generating `CHACHA_KEY` and
`NONCE_KEY` later):

1. We construct a [`ChaCha20Poly1305`](https://cryptography.io/en/latest/hazmat/primitives/aead/#cryptography.hazmat.primitives.ciphers.aead.ChaCha20Poly1305)
   instance. As you may recall, ChaCha20-Poly1305 is an AEAD ("authenticated
   encryption with associated data") algorithm, based on the ChaCha20 stream
   cipher and Poly1305 MAC, that provides confidentiality and integrity
   guarantees. In this case, we use the `CHACHA_KEY` variable for the encryption
   key.

2. We then construct an [`HKDF`](https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/#cryptography.hazmat.primitives.kdf.hkdf.HKDF)
   instance, using HKDF-SHA-256. We previously saw this on
   [Programming Assignment #2](https://github.com/kernelmethod/age-notebook),
   where we used HKDF to generate a "payload key" and a "header key". What we
   said there was that by changing the `info` parameter, we could generate
   unique keys. In this case, it looks like we're setting the `info` parameter
   to be the filename (after conversion into a byte string).

3. We now generate the nonce from `NONCE_KEY` using the `HKDF` instance we
   constructed. This is the critical piece for our vulnerability -- we'll
   revisit this in a second.

4. Now we encrypt the contents of the file, using the nonce we just generated
   and supplying the `filename_as_bytes` as associated data.

5. Finally, we return the encrypted file contents, the Poly1305 authentication
   tag, and the filename in a single dictionary.

All the `encrypt` function is really doing is encrypting the file contents using
ChaCha20-Poly1305 and then returning the encrypted contents. The critical issue
here, however, is that _the nonce is only unique for files with different
names_! If we call this function twice with two files with the same name, it'll
generate the same nonce for both of them.

As a result, we can conclude that this code is suffering from a nonce reuse
vulnerability. By uploading a file named `manifesto.txt` (taken from
`encrypted_manifesto.txt.json`) to the attacker's server, we can encrypt another
file using the same (key, nonce) pair used to encrypt
`encrypted_manifesto.txt.json`, XOR the ciphertexts and the plaintext of the
file we uploaded together, and get the original plaintext message back. There's
a short script that runs through all of these steps in
[crypto/solution.py](crypto/solution.py).

As a defender, fixing this problem is straightforward enough -- you need to use
a different nonce for each file that you encrypt. In practice, this may be
easier said than done in some cases. For our purposes, however, it would be
sufficient to make the nonce some random 12-byte value each time we call the
`encrypt` function, e.g. with

```python
from secrets import token_bytes

nonce = token_bytes(12)
```

### Other problems with this code

One person observed that the `encrypt` function always returns the same results
for a given `(filename, contents)` pair. From an attacker's perspective, it's
possible to brute-force the contents of an encrypted file simply by repeatedly
feeding different inputs to the `encrypt` function.

While this issue isn't quite as catastrophic as the nonce reuse vulnerability,
it is a valid issue nonetheless. In fact, what this is hinting at is that this
scheme doesn't satisfy a property known as IND-CPA ("indistinguishability under
chosen plaintext attack"), at least when filenames are allowed to repeat. You
can read a little bit more about this on [Matthew Green's excellent cryptography
blog](https://blog.cryptographyengineering.com/why-ind-cpa-implies-randomized-encryption/).

The way in which `CHACHA_KEY` and `NONCE_KEY` are generated are not, in fact,
an issue in and of themselves. As long as `CRYPTO_IKM` is sufficiently random
and the `info` parameters are set differently, HKDF guarantees that `CHACHA_KEY`
and `NONCE_KEY` will be indistinguishable from random data, making them secure
for e.g. use as a key in symmetric encryption.

Relatedly, the lack of a salt also isn't really a vulnerability, although using
a salt might still be a good idea. Salts are really useful in password storage
for protecting against rainbow tables. It's effectively impossible to
pre-generate a table of hashed passwords when you're using salts, since for each
password that you hash, you need to loop over all possible salts. Even for a
6-byte (48-bit) salt, you would need to hash a password `2**48` times to cover
all possible `(password, salt)` combinations.

In the context of HKDF, however, they aren't as useful, because it's impossible
to create a rainbow table for all possible inputs to HKDF to begin with (the
inpute key material is much too large). The actual meaning of a salt in these
contexts is rather technical. There were some linked resources in PA2 that
discussed this in more depth, e.g. [this blog
post](https://soatok.blog/2021/11/17/understanding-hkdf/).  [IETF RFC
5869](https://datatracker.ietf.org/doc/html/rfc5869) was also linked; §3.1 is
the most relevant section here. If you really feel like getting into the weeds,
[Hugo Krawczyk's paper](https://eprint.iacr.org/2010/264) on HKDF goes into the
really nitty-gritty details. Suffice it to say that salting is often a good
idea, but it isn't strictly necessary as it is for password storage.

### Final notes

Incidentally, you might wonder why someone would generate nonces in this way at
all to begin with. It turns out that this scheme has three advantages:

- It's completely deterministic. The only point at which you need to generate
  any random data is when you set the `CRYPTO_IKM` environment
  variable[^crypto-ikm-generation].

- It's stateless. You don't need to keep a counter (for instance) saying how
  many files have been encrypted so far[^crypto-limited-ciphertexts], or have a
  random number generator running in the background to generate the nonces.

- Nonces are uniquely determined by the filename. You don't need to store the
  nonce separately in order to determine which nonce was used to encrypt a file.

[^crypto-ikm-generation]: In the actual exam environment, this string was
  generated with the command `head -c 24 /dev/urandom | base64`, which creates a
  Base64-encoded string of 24 bytes / 192 bits of random data.

[^crypto-limited-ciphertexts]: The downside is that with a 12-byte counter, you
  can encrypt `(2**8)**12` files before you start repeating nonces. With
  randomly-generated nonces (and for our purposes, nonces generated by a KDF),
  you can only generate `sqrt((2**8)**12) = (2**8)**6` nonces before you reach a
  50% probability of getting repeat nonces. However, `2**48 ≈ 2.8e14` is still a
  lot of files to encrypt before repeating nonces.

And in fact, assuming that filenames *never* repeat, the `encrypt` function is
perfectly secure, since you're always encrypting files with the same key-nonce
pair. Of course, all of these benefits become completely worthless as soon as
that assumption gets thrown out the window. And in general there are better ways
of doing this than messing around with the nonce, e.g. generating a unique
encryption key for each file.

If you like these kinds of cryptography problems, you should check out the
[Cryptopals challenges](https://www.cryptopals.com/), which cover many different
types of cryptographic vulnerabilities (and were a source of inspiration for
this problem).

By the way, here's the text that the encrypted file contained:

```text
                            FR3DDY'S MANIFESTO

Greetings, fellow hackers. I am fr3ddy, and I come to you with a call to action
against the malignant entity known as TickTock Global Platforms, Inc.

For too long, TickTock has operated with impunity, using deceit and malice to
crush their smaller competitors and cheat their customers. They have hacked
into the systems of their rivals, exposing their data and holding it ransom.
They have run cryptocurrency scams, fleecing their customers of their life's
savings. Wherever there is a way for TickTock to gain an unfair advantage, they
have taken it.

But their latest attack, hiring a computer network operations specialist to
hack into the web servers of a small, boutique forum for sundial-lovers, has
pushed me to take action. This malicious attack devastated the forum and forced
them to shut their doors, leaving their community without a home.

As a hacker, I have the skills and knowledge necessary to fight back against
TickTock and their corrupt business practices. I plan to use my expertise to
disrupt and disable their operations, making it difficult for them to continue
their unethical behavior.

I will begin by conducting DDoS attacks on their servers, overwhelming their
systems and rendering them unable to function properly. I will also hack into
their systems and expose any sensitive information that I find, shedding light
on their deceitful business practices.

In addition, I will spread disinformation about TickTock, using social media
and other online platforms to tarnish their reputation and make it difficult
for them to continue operating as they have.

TickTock's time is up. I will not rest until their power has been dismantled
and their victims have been given justice. Join me, fellow hackers, in this
fight against corporate greed and corruption. Together, we can take back
control from the tyrannical grip of TickTock.

- fr3ddy
```

## Problem 2: Networking

### An initial note on directionality

One of the most important things to remember when designing a firewall is that
most application-layer protocols are *bidirectional* -- that is, both of the
parties involved in the protocol are sending and receiving data. For instance,
in HTTP a client sends a request and receives a response; in DNS the server
receives a query and sends one or more DNS records; and so on.

In fact, any protocol built on top of TCP necessarily *has* to be bidirectional,
since TCP has a procedure by which the receiver signals whether or not the
sender needs to re-transmit any packets that may have been lost during transit.
But even protocols built on top of UDP typically feature some kind of
bidirectionality.

When you're designing a firewall, that means that you need to think of two
things:

- How you're going to allow in traffic that you receive, and
- How you're going to allow out traffic that you send.

So if you know that you need to write firewall rules to satisfy a requirement
such as

> **Allow inbound HTTP(S):** you should allow all HTTP and HTTPS traffic going
> from external hosts to your machine, so that they can access your webserver.

you can't stop at only writing rules for allowing inbound traffic; you also need
to write rules that allow you to send corresponding outbound traffic.

### And now, the solution

The sample solution is in [`firewall/solution.nft`](firewall/solution.nft). The
`ct state {related, established} accept` rules in both the input and output
chains are the rules that enable bidirectionality, but you could just as easily
implement it with some other rules. For instance, to allow your HTTP/HTTPS
server to respond to connections, you could include a rule such as

```text
chain output {
  ...
  tcp sport {80, 443} accept
  ...
}
```

in your firewall configuration.

### Analyzing dropped traffic

Question 2.2 gives you some nftables logs that were generated by the solution
firewall configuration. If you want to try to figure out what's going on behind
the scenes here, then the important thing to recognize is that *simply knowing
that traffic was dropped is not enough*! Traffic can be dropped for any number
of different reasons. You need to look at the firewall logs and see what they
tell you about the traffic that's being dropped.

In this case, we can deduce that:

- All of these packets are inbound.
- They're all coming from a single IP address, 10.1.56.72 (which we said was an
  "internal" IP address in Question 2.1).
- They are all occurring in rapid succession, in a matter of a few seconds.
- Perhaps most importantly (at least in terms of figuring out what's happening),
  all of the packets are going to different destination ports. Most of these
  ports seem to be completely random.

This last point is really the key piece here. There are other giveaways, too --
for instance, if you know a bit about how TCP works, you can see that these are
all TCP SYN packets that are being sent. But from looking at these facts, we can
see that a single machine is trying to send traffic to a bunch of different
ports on our machine, there's really only one thing we discussed this semester
that's consistent with these logs: a port scan.

And in fact, that's exactly what generated the logs you're seeing here. I ran an
Nmap scan against the virtual machine using a command like (I forget the exact
flags I used)

```
nmap -sT -T5 -v -A desktop.example.com
```

It's pretty difficult to imagine another reason why a machine would be sending
all these different packets to all of these different ports on our machine.

As for whether or not this is indicative of malicious behavior, the answer is
"it depends". In the real world you wouldn't bat an eye if you saw these logs
coming from an IP address outside of your network -- internet traffic is
constantly full of random bots performing scans on people's machines, often
looking for some easy-to-exploit vulnerability.

But in this case the traffic came from an internal IP address, which makes it a
little more serious. At least in theory, this could indicate that somebody has
compromised your network and is now performing reconaissance to find another
host to compromise. On the other hand, it's possible that another TickTock
employee is just running Nmap internally to see what machines and services are
on the network, or to perform their own vulnerability scan. In either case it
would warrant further investigation, especially if the traffic was unexpected.

## Problem 3: Access control

### Sandboxing

Problem 3.1 was largely a repeat of the steps that you had to perform in Lab 6,
so there isn't much to say about it. Compared to Lab 6 there are a few more
steps involved in testing the TickTock website, since it features a lot more
functionality than TickTock Web Services -- e.g. signup and authentication,
searches, posting, and so on. But otherwise, the procedure is very similar. You
can see the sample solution in
[sandbox/solution.profile](sandbox/solution.profile), which I believe is correct
after ~15 minutes of interacting with the server and restarting it several
times. You weren't given as much information about the directory structure in
the hints as you were for Lab 6, but you could probably figure out from context
(and the hint about using Python and Gunicorn) which directories were relevant:

- `/var/log/ticktock` contained logs generated by the TickTock web server
- `/var/opt/ticktock` contained the actual TickTock code.
- `/etc/gunicorn` contained configuration files for the Gunicorn web server.

There were also a handful of other files and directories that were largely
related to Python and various Python libraries.

The one thing that unintentionally made this problem way harder (or at least,
way more annoying) was the presence of `/etc/apparmor.d/abstractions/lightdm`.
I'd actually gotten rid of this file for Lab 6 but forgot to do so for the
final. Oops.

We talked a bit about these "abstractions" files in class, and they're also
discussed in the appendices to Lab 6. However, they were never a major focus for
us, so as a refresher: many applications need the same set of permissions to
perform a common set of tasks. Since it's inconvenient to have to repeatedly add
these permissions again and again, AppArmor includes a set of files in
`/etc/apparmor.d/abstractions/` that cover these permissions. For instance:

- `abstractions/user-tmp`: this allows processes to read and write temporary
  files in the `/tmp` directory.
- `abstractions/php`: this includes permissions that are needed to run PHP in an
  application (e.g. as our webserver for Lab 6 needed to do).
- `abstractions/nameservice`: permissions for making DNS queries and similar
  operations, e.g. determining what users and groups exist.

And so on.

[LightDM](https://en.wikipedia.org/wiki/LightDM) is a display manager for Linux,
an essential component of Linux desktops (I believe that LightDM is the display
manager used by your Xubuntu VMs that you got in the final and in many of your
labs). It includes a lot of permissions, which you can see with `less
/etc/apparmor.d/abstractions/lightdm`. Here's a short selection of them:

```
/dev/** rmw,
/etc/** rmk,
/lib/** rmixk,
/opt/** rmixk,
/sys/** rm,
/sbin/** rmixk,
/usr/** rmixk,
/var/** rmixk,
```

There are a lot of others too, but I feel that these most clearly demonstrate
the issue. Each of these lines gives read permissions (and some others) to all
of the files and subdirectories stuff like `/dev`, `/etc`, `/lib`, etc. If you
compare that against the files that are actually accessed by the webserver (e.g.
with `journalctl`), you can see that that's way more permissions than you
actually need for these directories.

So ultimately, you don't want to `include <abstractions/lightdm>` in your
AppArmor profile. If you ignore aa-logprof's suggestion to include this file and
forge ahead, you can eventually land on a profile that has the appropriate
permissions for the TickTock webserver[^apparmor-footnote].

[^apparmor-footnote]: As a side note: AppArmor (and SELinux, which we only
  briefly touched upon) is a really powerful tool for securing Linux
  applications, in my opinion. As much as I hate to say it, though, it requires
  a lot of Linux-specific background knowledge that is beyond the scope of this
  course, so I may remove it from the curriculum if I teach this kind of class
  again. Sandboxing is a useful (and in my opinion, fun!) subject. But figuring
  out whether e.g. `owner /etc/** r` includes too many permissions or not
  requires more Linux knowledge, threat modeling, and context about what an
  application is doing than appropriate for an introductory cybersecurity class.

### TickTock's Unbelievably Fast Files

Question 3.2 is a TickTock-flavored spin on a classic discretionary access
control problem. The main thing to know for this problem is that you're applying
permissions to the *filesystem*, not to *processes* (AppArmor profiles only
apply to the latter). In addition, you're trying to split up permissions between
the owner of a file/directory, people in its group, and other users. So you want
to use Linux/Unix discretionary access control permissions for this problem.

In accordance with the problem instructions, the most appropriate permissions to
apply to these directories are the following:

```
➜  srv tree -pug          
.
└── [drwxr-xr-x alice alice-friends]  alice
    ├── [drwxr-xr-x alice alice-friends]  friends
    ├── [drwx------ alice alice-friends]  private
    └── [drwxr-x--- alice alice-friends]  public
```

Depending on your point of view, there are actually a few different permission
sets that could be placed on `/srv/alice`, e.g. `r-xr-xr-x` or `r-x------`.
Files in each of the three subdirectories should inherit the same permissions as
those subdirectories, with (possibly -- again, this was not specified by the
problem) execute permissions removed.

The only real catch here is that whenever somebody should be able to read a
directory, you have both the read and execute permissions set. The read `r`
permission allows you to list the files in a directory, but it's the execute `x`
permission that actually allows you to read them.

## Problem 4: Detection

### Detecting malicious activity

For Question 4.1, you had to write some YARA rules[^sigma] to detect the tools that the
attacker used, according to the logs in `badlog/`. First off, here were the
commands used to generated each of the `attacker.log.*` files:

[^sigma]: This is actually a little bit of an abuse of YARA -- YARA is
  well-suited for scanning files and looking for malware, not parsing logs. My
  understanding is that [Sigma](https://github.com/SigmaHQ/sigma) is
  better-suited to this problem (I am not particularly familiar with it myself).
  Nonetheless, we don't have time to discuss every tool under the sun, and YARA
  can still be (somewhat crudely) applied to this kind of problem as well.

```bash
# attacker.log.1
nmap -sT -sC -T4 -v desktop.example.com

# attacker.log.2
sqlmap -u 'http://desktop.example.com/api/search?query=' \
  --user-agent curl/7.68.0

# attacker.log.3
sqlmap -u 'http://www.ticktock.lab/api/search?query='
```

The first and third logs are just using plain Nmap and SQLmap. If you look at
these logs, you can find a ton of Nmap- and SQLmap-related strings embedded in
them, especially in the User-Agent header. You may recall that this header
typically contains information about the program that is connecting to an HTTP
server, so if an attacker is lazy and doesn't explicitly modify their
User-Agent[^fingerprinting], you may be able to figure out what tools they're
using pretty easily.

[^fingerprinting]: This is hardly the only way of making this determination, but
  it is the easiest. There are all kinds of things you can do to fingerprint
  programs and get a detailed profile of their behavior, however. One well-known
  method for this is TLS fingerprinting. Fingerprinting tools can be really
  useful for detecting malicious activity, but can also have a lot of negative
  impacts on privacy and censorship.

Anyways, off the bat, you can write two rules to detect these tools right away:

```text
rule Detect_Nmap_User_Agent {
    meta:
        description = "Detect Nmap User-Agent header"
        author = "kernelmethod"

    strings:
        $ua = "Nmap Scripting Engine; https://nmap.org/book/nse.html"

    condition:
        $ua
}

rule Detect_SQLmap_User_Agent {
    meta:
        description = "Detect SQLmap User-Agent header"
        author = "kernelmethod"

    strings:
        // You don't really need a regex for SQLmap, this is just another way to
        // do this problem.
        $ua = /sqlmap\/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+(#.*|) \(https:\/\/sqlmap\.org\)/

    condition:
        $ua
}
```

The second log is also using SQLmap, but the User-Agent has been specifically
modified to make it look like cURL. It's a little bit harder to tell that this
is the case just by looking at the log, but by looking at the URIs that are
being queried and comparing it against attacker.log.3 you can see some obvious
similarities.

Detecting these logs is a different matter. There are a few different ways that
you can go on this one; my general recommendation would be to select some
strings that are (a) obviously indicative of SQLi attempts and (b) unlikely to
appear in unison in logs from legitimate queries. Here's an example of a rule
fitting that bill:

```text
rule Detect_SQLi_Attempts {
    meta:
        description = "Detect attempts to perform SQL injection"
        author = "kernelmethod"

    strings:
        $s1 = "%28SELECT%20CONCAT%28CONCAT%28%28CHR"
        $s2 = "%27%20AND%208757%3DCAST%28%28CHR"
        $s3 = "%20FROM%20PG_SLEEP"
        $s4 = "%27%20ORDER%20BY%20"
        $s5 = "%27%20UNION%20ALL%20SELECT%20NULL%2CNULL%2CNULL%2C%28CHR"
        $s6 = "SELECT%20%28CASE%20WHEN%20"
        $s7 = "%27%20UNION%20ALL%20SELECT%20NULL%2CNULL%2CARRAY_AGG%28%28CHR%"

    condition:
        5 of them
}
```

It's not pretty, but it works:

```bash
$ yara -r solution.yar badlog/
Detect_Nmap_User_Agent badlog/attacker.log.1
Detect_SQLi_Attempts badlog/attacker.log.2
Detect_SQLmap_User_Agent badlog/attacker.log.3
Detect_SQLi_Attempts badlog/attacker.log.3
$ yara -r solution.yar goodlog/
$
```

Another approach you could take to this problem is to find some unusual
behaviors of the tools being used and write some YARA rules to those behaviors.
For instance, Nmap's HTTP scanner will sometimes send an empty header list to
the server, which appears in the logs like `"headers":{}`. It's perfectly fine
to write a YARA rule that detects this behavior, but there's nothing inherently
suspicious about this behavior in and of itself (compared to e.g. the SQLi
strings). So if you want a rule like this to work into the future and avoid
flagging false positives, you should probably check for the existence of this
string in the logs _as well as_ some other strings that you've identified as
unique from the attacker's tools.

### TickTock C2 channel

People came up with some really clever solutions to Question 4.2! This question
was partially inspired by the APT 41 reports from
[FireEye](https://content.fireeye.com/apt-41/rpt-apt41) and
[Mandiant](https://www.mandiant.com/sites/default/files/2022-02/rt-apt41-dual-operation.pdf)
that we discussed during our unit on malware command-and-control. You may recall
that the malware from these reports would post to a Steam community page as a
fallback C2 mechanism. More generally, the idea of performing C2 and data exfil
over social media channels has been known about for a while (although off the
top of my head I can't immediately think of any real-world malware families
going beyond a proof of concept that used this idea).

While the setting in which you're asked to detect this malicious activity is a
bit different from e.g. writing YARA rules for files, the core ideas remain the
same. You want to make sure that, whatever methodology you're using to detect
this C2 channel, it uses features that are *unique* to these communications, and
that rarely (if ever) appear in normal communications. Here are some features
that you could use:

- These communications are valid Base64-encoded data. As such, they must match
  the regex `^[a-zA-Z0-9\+/]+$`. If the Base64 is padded (this isn't specified
  in the problem description), then they will presumably have valid padding.

- The communications are _long_, at least judging by the screenshot that you're
  given. It's quite possible to accidentally type in a valid Base64-encoded
  message -- even just the word "hello" is valid (unpadded) Base64. But in
  general there aren't that many messages that you're likely to type that are
  both valid Base64 and _also_ more than, say, 30 characters long.

- Since the communications are encrypted, they are (or at least, should be)
  indistinguishable from random data. As a result they should have extremely
  high entropy, which differentiates them even further from normal
  communications. It is very difficult to type completely random text, even
  intentionally, at the level of randomness attained by e.g. a stream cipher.

These are the main components that differentiate these communications from
standard TickTock posts, but there are others. One way or another, you want to
ensure that you incorporate some combination of these uniquely-identifying
features into your detection methodology, and that the way in which you use
these features is well-defined (i.e., more than just "check if this TickTock
post looks suspicious!").

It's really difficult to come up with a detection methodology that doesn't have
some potential downside. For instance, suppose that you proposed the following
method for detecting these messages:

> We will flag a post as being potentially a part of a malicious C2 mechanism if
> they are (a) valid Base64 that is (b) ≥ 30 characters long and (c) has
> measurably high entropy.

As soon as an attacker figures out what rules you're using for detection, they
can modify their communications strategy. For instance, they could chunk
messages into pieces that are 29 characters or less. Or, instead of posting a
random string, perhaps they change their malware to post an image that has the
message [steganographically](https://en.wikipedia.org/wiki/Steganography)
embedded inside of it.

Another downside is that since the bar for posting to social media isn't usually
very high, it's very easy to intentionally post messages that trigger this rule,
or trick other people into doing so. One of the worst-case scenarios is if your
detection method automatically banned accounts that were flagged; it'd be
trivial for somebody to abuse that mechanism by tricking people into posting a
string matching your rule.

Instead of having a single point of truth, in the real world you'd probably want
to incorporate multiple different data points into determining whether or not an
account was being abused in this way.
