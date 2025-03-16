from typing import Annotated

from pydantic import Field, validate_call


@validate_call
def convert_alphabet_index(alphabet: Annotated[str, Field(min_length=1, max_length=1, pattern=r'^[a-zA-Z]+$')]):
    return ord(alphabet.upper()) - ord('A')


if __name__ == '__main__':
    abc = convert_alphabet_index('z')
    print(abc)
