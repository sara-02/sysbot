import codecs


def decoder(token_name, encrypted_token):
    token = codecs.decode(encrypted_token, 'rot13')
    print token_name + "=" + token
