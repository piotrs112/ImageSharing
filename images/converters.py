from hashids import Hashids


class HashIdConverter:
    min_length=64
    h = Hashids(min_length=min_length, salt="220e8b256ecf28b392284f07d8610f25db127cae4b788cf1bdf11650beb5b732")

    regex = r'[{}]{{}}'.format(Hashids.ALPHABET, min_length)

    def to_python(self, value):
        return h.decode(value)

    def to_url(self, value):
        return h.encode(value)

class FilenameToPkConverter:
    regex = r'uploads/'