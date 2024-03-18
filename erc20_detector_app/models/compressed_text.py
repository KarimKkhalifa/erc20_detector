import gzip

from sqlalchemy.types import TypeDecorator, LargeBinary


class CompressedText(TypeDecorator):
    """A type for compressing text fields."""

    impl = LargeBinary

    def process_bind_param(self, value, dialect):
        """Compress text data on save."""
        if value is not None:
            value_bytes = value.encode('utf-8')  # Encode the text to bytes
            compressed_value = gzip.compress(value_bytes)
            return compressed_value
        return value

    def process_result_value(self, value, dialect):
        """Decompress text data on load."""
        if value is not None:
            decompressed_value = gzip.decompress(value)
            return decompressed_value.decode('utf-8')  # Decode bytes back to string
        return value
