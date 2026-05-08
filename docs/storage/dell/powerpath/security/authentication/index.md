# PowerPath — Authentication

> Authentication documentation for PowerPath will be documented here.

## Overview

PowerPath does not implement its own authentication system. Access to `powermt` commands is controlled entirely by the host operating system's authentication mechanisms.

- On Linux, `powermt` commands require root or sudo privileges
- On Windows, PowerPath management requires Local Administrator rights
- Service accounts used for automation should be granted only the minimum required permissions via sudoers (Linux) or local group membership (Windows)

Refer to the [Access Control](../access-control/) page for role definitions and sudoers configuration examples.
