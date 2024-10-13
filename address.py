class Address:
    def __init__(self, addr):
        match addr:
            case str():
                self.dec = Address.addr2dec(addr)
                self.str = addr
            case int():
                self.dec = addr
                self.str = Address.addr2str(addr)
            case Address():
                self.dec = addr.dec
                self.str = addr.str
            case x:
                raise TypeError(
                    f'Converting value {x} of type {type(x)}'
                    ' to Address not supported'
                )

    def conversion_decorator(func):
        return lambda self, other: func(self, Address(other))

    @conversion_decorator
    def __add__(self, other):
        return Address(self.dec + other.dec)

    @conversion_decorator
    def __sub__(self, other):
        return Address(self.dec - other.dec)

    @conversion_decorator
    def __or__(self, other):
        return Address(self.dec | other.dec)

    @conversion_decorator
    def __xor__(self, other):
        return Address(self.dec ^ other.dec)

    @conversion_decorator
    def __and__(self, other):
        return Address(self.dec & other.dec)

    def __invert__(self):
        return Address(~self.dec)

    def __index__(self):
        return self.dec

    def __format__(self, format_spec):
        return format(self.dec, format_spec)

    def __repr__(self):
        return f"Address('{self.str}')"

    @staticmethod
    def addr2dec(addr):
        addr = (int(o) for o in addr.split('.')[::-1])
        return sum(o << i*8 for i, o in enumerate(addr))

    @staticmethod
    def addr2str(dec):
        octets = tuple(dec >> i*8 & 255 for i in range(4))
        return '.'.join(str(o) for o in octets[::-1])

    def get_broadcastaddr(network_address, subnet_mask):
        return Address(network_address) | ~Address(subnet_mask)

    def get_networkaddr(broadcast_address, subnet_mask):
        return Address(broadcast_address) & subnet_mask

    def get_subnetmask(network_address, broadcast_address):
        return ~(Address(network_address) ^ broadcast_address)

    @staticmethod
    def calculate_subnetmask(addrcnt):
        return (
            Address('255.255.255.255') -
            (2 ** ((addrcnt - 1).bit_length()) - 1)
        )
