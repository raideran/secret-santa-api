import re


def email_validator(value):
    """Validate an email address.
    """

    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^`{}|~\w]+(\.[-!#$%&'*+/=?^`{}|~\w]+)*\Z"  # dot-atom
        # quoted-string
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]'
        r'|\\[\001-\011\013\014\016-\177])*"\Z)',
        re.IGNORECASE | re.UNICODE,
    )

    domain_regex = re.compile(
        # domain
        r"(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+" r"(?:[A-Z]{2,6}|[A-Z0-9-]{2,})\Z"
        # literal form, ipv4 address (SMTP 4.1.3)
        r"|^\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)"
        r"(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]\Z",
        re.IGNORECASE | re.UNICODE,
    )

    domain_whitelist = ("localhost",)

    if not value or "@" not in value:
        return False

    user_part, domain_part = value.rsplit("@", 1)

    if not user_regex.match(user_part):
        return False

    if domain_part not in domain_whitelist:
        if not domain_regex.match(domain_part):
            try:
                domain_part = domain_part.encode("idna").decode("ascii")
            except UnicodeError:
                pass
            else:
                if domain_regex.match(domain_part):
                    return value
            return False

    return value
