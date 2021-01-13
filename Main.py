import requests
import hashlib
import getpass


# Ask for password and return SHA-1 hash.
def get_hashword():
    hashobj = hashlib.sha1()
    hashobj.update(getpass.getpass().encode("utf-8"))
    return hashobj.hexdigest().upper()


# Anonymously query API with generated hash, and return list of matching hashes.
def request_api_data(_hash):
    url = "https://api.pwnedpasswords.com/range/" + _hash[:5]
    res = requests.get(url)
    return res.text


# Generator that supplies the hacked hash suffixes and their hack counts, one at a time.
def res_generator(_hash):
    for line in request_api_data(_hash).splitlines():
        yield line.split(":")


# Check if password hash is in list of returned hashes.
def check_hash(_hash):
    hashtuple = res_generator(_hash)
    while True:
        try:
            hashtail, count = next(hashtuple)
            if _hash[5:] == hashtail:
                print(f"Password has been hacked {count} times before. Try another password.")
                break
        except StopIteration:
            print("This password seems okay. Nice One!")
            break


if __name__ == '__main__':
    myhash = get_hashword()
    check_hash(myhash)
