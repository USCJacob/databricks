
class IpFirewallCoverageChecker:
    def __init__(self, rules):
        self.rules = []
        for action, cidr in rules:
            is_allowed = (action == "ALLOW")
            if "/" in cidr:
                ip_str, prefix_str = cidr.split("/")
                prefix = int(prefix_str)
            else:
                ip_str = cidr
                prefix = 32
            ip_int = self.ip_to_int(ip_str)
            mask = ((1 << prefix) - 1) << (32 - prefix)

            network = ip_int & mask

            self.rules.append((is_allowed, network, mask))

    def AllowAccess(self, ip: str):
        ip_int = self.ip_to_int(ip)
        for is_allowed, network, mask in self.rules:
            if (ip_int & mask) == network:
                return is_allowed

    def ip_to_int(self, ip):
        a, b, c, d = map(int, ip.split("."))
        return (a << 24) | (b << 16) | (c << 8) | d


class IpFirewallCoverageChecker:
    def __init__(self, rules):
        self.rules = []
        for action, cidr in rules:
            is_allowed = (action == "ALLOW")
            start, end = self.cidr_to_range(cidr)
            self.rules.append((is_allowed, start, end))

    def canFullyAllow(self, cidr):
        start, end = self.cidr_to_range(cidr)
        remaining = [(start, end)]
        for is_allowed, L, R in self.rules:
            if is_allowed:
                remaining = self.subtract_intervals(remaining, L, R)
            else:
                if self.have_overlaps(remaining, L, R):
                    return False
        return len(remaining) == 0

    def ip_to_int(self, ip):
        a, b, c, d = map(int, ip.split("."))
        return (a << 24) | (b << 16) | (c << 8) | d

    def have_overlaps(self, remaining, c, d):
        for a, b in remaining:
            L = max(a, c)
            R = min(b, d)
            if L <= R:
                return True
        return False

    def subtract_intervals(self, remaining, c, d):
        nxt = []
        for a, b in remaining:
            L = max(a, c)
            R = min(b, d)
            if L > R:
                nxt.append([(a, b)])
                continue
            if a <= L - 1:
                nxt.append((a, L - 1))
            if b >= R + 1:
                nxt.append((R + 1, b))
        return nxt

    def cidr_to_range(self, cidr):
        if "/" in cidr:
            ip_str, prefix_str = cidr.split("/")
            ip_int = self.ip_to_int(ip_str)
            prefix = int(prefix_str)
        else:
            ip_str = cidr
            ip_int = self.ip_to_int(ip_str)
            prefix = 32

        mask = ((1 << prefix) - 1) << (32 - prefix)
        network = mask & ip_int

        size = 1 << (32 - prefix)

        left = network
        right = network + size - 1

        return (left, right)

rules = [
    ["ALLOW", "10.0.0.0/26"],   # covers 10.0.0.0 ~ 10.0.0.63
    ["DENY",  "10.0.0.64/26"],  # overlaps remaining part of target -> should fail immediately
    ["ALLOW", "10.0.0.64/26"],  # too late
    ["ALLOW", "10.0.0.128/25"],
]
target = "10.0.0.0/24"

checker = IpFirewallCoverageChecker(rules)
print(checker.canFullyAllow(target))  # False