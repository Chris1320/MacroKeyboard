#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MIT License
Copyright (c) 2020 Chris1320

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import zlib
import json
import base64
import hashlib

from Cryptodome import Random
from Cryptodome.Cipher import AES

VERSION = "0.0.2.1"  # Module version


class AES256(object):
    """
    The class that contains methods for working with AES-256.

    Credits to the people from StackOverflow! LMAO

    https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
    """

    # This class is from my `Ciphers/aes.py` module.

    def __init__(self, key, encoding="utf-8"):
        """
        The initialization method of AES256() class.

        :param str key: The key/password of the message.
        """

        self.VERSION = "0.0.1.2"

        self.bs = AES.block_size  # The block size
        self.encoding = encoding  # The encoding to be used when calling `encode()` and `decode()`.
        self.key = hashlib.sha256(key.encode(self.encoding)).digest()  # The hashed key

    def encrypt(self, message):
        """
        Encrypt <message> using <self.key> as the key/password.

        :param str message: The message to encrypt.

        :returns bytes: The ciphertext.
        """

        padded_message = self._pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        emessage = padded_message.encode(self.encoding)  # Encoded message
        ciphertext = base64.b64encode(iv + cipher.encrypt(emessage))

        return ciphertext

    def decrypt(self, ciphertext):
        """
        Decrypt <ciphertext> using <self.key> as the key/password.

        :param bytes ciphertext: The ciphertext to decrypt.

        :returns str: The plaintext version of the ciphertext.
        """

        ciphertext = base64.b64decode(ciphertext)
        iv = ciphertext[:AES.block_size]  # Get the iv from the ciphertext
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext[AES.block_size:])
        plaintext = self._unpad(decrypted).decode(self.encoding)

        return plaintext

    def _pad(self, s):
        """
        Add a padding to <s>.
        """

        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        """
        Remove padding from <s>.
        """

        return s[:-ord(s[len(s)-1:])]

class Version1():
    """
    The class containing methods to use the version 1 configuration file.
    """

    def __init__(self, config_path="data/config.dat", isbase64=False, encoding="utf-8"):
        """
        The initialization method for ConfigHandler() class.

        :param str config_path: The path of the configuration file to use.
        :param bool isbase64: True if the configuration file is encoded via Base64.
        :param str encoding: The encoding to be used.
        """

        self.VERSION = "0.0.1.1"  # Parser version
        self.config_path = config_path
        self.isbase64 = isbase64
        self.encoding = encoding

    def _open_config_file(self):
        """
        Open the config file.

        :returns str: The configuration file data.
        """

        try:
            with open(self.config_path, 'r') as fopen:
                data = fopen.read()

        except(FileNotFoundError, IOError, EOFError,
                PermissionError, IsADirectoryError):
            raise IOError("Error reading the configuration file!")

        else:
            if self.isbase64 == True:
                try:
                    data = base64.b64decode(data)

                except(TypeError, ValueError, UnicodeDecodeError):
                    raise IOError("The configuration file is corrupt or decrypted!")

                else:
                    try:
                        return str(data.decode(self.encoding))

                    except(TypeError, ValueError,UnicodeDecodeError):
                        raise IOError("The configuration file is corrupt or decrypted!")

            else:
                return data

    def _save_config_file(self, config_data):
        """
        Save the config file.

        :param str config_data: The whole content of the configuration file.

        :returns int: Error code
        """

        try:
            with open(self.config_path, 'w') as fopen:
                fopen.write('')

        except(FileNotFoundError, IOError, EOFError,
               PermissionError, IsADirectoryError):
            raise IOError("Error writing to the configuration file!")

        else:
            try:
                if self.isbase64 == True:
                    with open(self.config_path, 'w') as fopen:
                        fopen.write(base64.b64encode(config_data.encode(self.encoding)).decode(self.encoding))

                else:
                    with open(self.config_path, 'w') as fopen:
                        fopen.write(config_data)

            except(FileNotFoundError, IOError, EOFError,
                   PermissionError, IsADirectoryError):
                raise IOError("Error writing to the configuration file!")

            else:
                return 0

    def get(self, data=None):
        """
        Get data from config file.

        :param str data: The key/name of the value you are looking for.

        :returns bool:
        :returns int:
        :returns float:
        :returns str:
        :returns void:
        """

        contents = self._open_config_file()

        if data is None:
            return None

        else:
            contents = contents.split('\n')

            for content in contents:
                if content.startswith('#'):
                    continue

                elif content.startswith(data + '='):
                    # This if-else statement below is *specially* for booleans.
                    # ! DEV0001: Might introduce bugs in the future!
                    if content.replace('\n', '').partition('=')[2].lower() == "true":
                        return True

                    elif content.replace('\n', '').partition('=')[2].lower() == "false":
                        return False

                    elif content.replace('\n', '').partition('=')[2].isdigit():
                        try:
                            return int(content.replace('\n', '').partition('=')[2])

                        except ValueError:
                            return content.replace('\n', '').partition('=')[2]

                    elif content.replace('\n', '').partition('=')[2].replace('.', '').isdigit():
                        try:
                            return float(content.replace('\n', '').partition('=')[2])

                        except ValueError:
                            return content.replace('\n', '').partition('=')[2]

                    elif content.replace('\n', '').partition('=')[2] == "None":
                        try:
                            return None

                        except ValueError:
                            return content.replace('\n', '').partition('=')[2]

                    else:
                        return content.replace('\n', '').partition('=')[2]

                else:
                    continue

    def set(self, variable=None, value=None):
        """
        Set a new value for `variable`.

        :param str variable: The variable name/key to modify/add.
        :param str value: The desired value of <variable>.

        :returns int, str: Error code and error description (if there is one.)
        """

        if variable is None or value is None:
            return 11

        else:
            try:
                variable = str(variable)
                value = str(value)

            except(TypeError, ValueError):
                return 11

            else:
                contents = self._open_config_file().split('\n')
                new_config = []
                for content in contents:
                    if content.startswith('#'):
                        new_config.append(content)

                    elif content.startswith(variable + '='):
                        new_config.append(variable + '=' + value)

                    elif content == "":
                        new_config.append('')

                    else:
                        new_config.append(content)

                result = ""
                for line in new_config:
                    if line == "":
                        result += ''

                    else:
                        result += line + '\n'

                try:
                    self._save_config_file(result)

                except Exception as error:
                    return 1, str(error)

                else:
                    return 0

    def new(self):
        """
        Create a new configuration file.

        :returns int, str: Error code and an error description, if there is one.
        """

        if os.path.exists(self.config_path):
            return 2651, "File already exists"

        new_config = [
            "# ConfigHandler configuration file",
            "# Configuration File Version: 0.0.1.0"
        ]
        result = ""
        for line in new_config:
            if line == "":
                result += ''

            else:
                result += line + '\n'

        try:
            self._save_config_file(result)

        except Exception as error:
            return 1, str(error)

        else:
            return 0

    def add(self, variable=None, value=None):
        """
        Add a new variable and set value for it.

        :param str variable: The variable name/key to modify/add.
        :param str value: The desired value of <variable>.

        :returns int, str: Error code and the error description if there is one.
        """

        if variable is None or value is None:
            return 11

        else:
            try:
                variable = str(variable)
                value = str(value)

            except(TypeError, ValueError):
                return 11

            else:
                contents = self._open_config_file().split('\n')
                new_config = []
                for content in contents:
                    if content.startswith('#'):
                        new_config.append(content)

                    elif content.startswith(variable + '='):
                        return 15

                    elif content == "":
                        new_config.append('')

                    else:
                        new_config.append(content)

                new_config.append(variable + '=' + value)

                result = ""
                for line in new_config:
                    if line == "":
                        result += ''

                    else:
                        result += line + '\n'

                try:
                    self._save_config_file(result)

                except Exception as error:
                    return 1, str(error)

                else:
                    return 0

class Version2():
    """
    The class containing methods to use the version 2 configuration file.
    """

    def __init__(self, configpath, epass=None):
        """
        The initialization method of Version2() class.

        :param str configpath: The path of the configuration file to use.
        :param str epass: The encryption password (Optional)
        """

        self.VERSION = "0.0.1.1"  # Parser version

        self.configpath = configpath
        self.__data = {
            "name": None,
            "author": None,
            "version": None,
            "compression": None,
            "encryption": None,
            "dictionary": None  # The encrypted form of the dictionary
        }
        self.__dictionary = None  # The decrypted form of the dictionary
        self.__epass = epass
        self.encoding = "utf-8"  # ? What if we include this inside config data?

        # A list of supported data types
        self.datatypes = ("str", "int", "float", "bool", "arr", "bin")
        self.array_datatypes = ("str", "int", "float", "bool", "bin")
        self.datatypes_conversion = {
            "str": (str,),
            "int": (int,),
            "float": (float,),
            "bool": (bool,),
            "arr": (list, tuple),
            "bin": (bytes,)
        }
        self.array_datatypes_conversion = {
            "str": (str,),
            "int": (int,),
            "float": (float,),
            "bool": (bool,),
            "bin": (bytes,)
        }

        # Configuration file fields and their types
        self.keynames = {
            "name": (str,),
            "author": (str,),
            "version": (str,),
            "compression": (str,),
            "encryption": (str,),
            "dictionary": (str,)
        }

        # A list of supported compression algorithms
        self.compressions = ("None", "zlib")  # `huffman` soon to be supported

        # A list of supported encryption algorithms
        self.encryptions = ("None", "aes256")

    def __b64encode(self, to_encode, return_bytes=False):
        """
        Encode <to_encode> using Base64.

        :param str to_encode: The string to encode.*
        :param int to_encode: The integer to encode.*
        :param float to_encode: The decimal to encode.*
        :param bool to_encode: The boolean to encode.*
        :param bytes to_encode: The bytes to encode.*
        :param bool return_bytes: If True, this method will return the result in `bytes`.

        *The supported data types (except str and bytes) are converted to str.
        *str data types are converted to bytes.

        :returns str: The string version of the <encoded> (data type `bytes`) variable.
        :returns bytes: The bytes version of the <encoded> variable.
        """

        if type(to_encode) in (str, int, float, bool):
            to_encode = str(to_encode).encode(self.encoding)

        elif type(to_encode) is bytes:
            pass

        else:
            raise ValueError("Unsupported data type.")

        encoded = base64.b64encode(to_encode)
        if return_bytes:
            return encoded

        else:
            return str(encoded.decode(self.encoding))

    def __b64decode(self, to_decode):
        """
        Decode <to_decode> using Base64.

        :param str to_decode: The string to decode.
        :param bytes to_decode: The bytes to decode.

        :returns bytes: The decoded form of <to_decode> in `bytes` data type.
        """

        if type(to_decode) is str:
            to_decode = to_decode.encode(self.encoding)

        elif type(to_decode) is bytes:
            pass

        else:
            raise ValueError("Unsupported data type.")

        return base64.b64decode(to_decode)

    def __readconfig(self):
        """
        Read the configuration file.

        :returns void:
        """

        with open(self.configpath, 'r') as f:
            self.__data = json.loads(self.__b64decode(f.read()))

    def __writeconfig(self):
        """
        Replace existing data from <self.configpath> with <self.__data>.

        :returns void:
        """

        # Check if `self.__data` values are valid.
        self._validate_data()

        # Write new data to `self.configpath`.
        with open(self.configpath, 'w') as f:
            f.write(self.__b64encode(json.dumps(self.__data, separators=(',', ':'))))

    def _validate_data(self, configdata=None):
        """
        Validate configuration data (data type `dict`).
        Raises `ValueError` if there is an invalid value in the data.
        Raises `TypeError` if `configdata` is invalid.

        :param dict configdata: The dictionary form of configuration data.

        :returns void:
        """

        if configdata is None:
            configdata = self.__data

        else:
            if type(configdata) is dict:
                pass

            else:
                raise TypeError("configdata must be a dictionary.")

        for key in self.keynames:
            if type(configdata[key]) not in self.keynames[key]:
                raise ValueError("The key does not have a valid value data type.")

            else:
                continue

    def __readdict(self):
        """
        Read the dictionary and store it in <self.__dictionary>.

        :returns void:
        """

        if type(self.__data["dictionary"]) is str:
            dictionary = self.__data["dictionary"].encode(self.encoding)

        elif type(self.__data["dictionary"]) is bytes:
            dictionary = self.__data["dictionary"]

        else:
            raise TypeError("Invalid dictionary!")

        if dictionary == b'':
            # A lazy guess if the dictionary is empty.
            self.__dictionary = {}
            return None

        # Decompression
        dictionary = self.__b64decode(dictionary)
        if self.__data["compression"] == "None":
            decompressed = dictionary

        elif self.__data["compression"] == "zlib":
            decompressed = zlib.decompress(dictionary)

        else:
            raise ValueError("Invalid compression algorithm name")

        # Decryption
        decompressed = self.__b64decode(decompressed)
        if self.__data["encryption"] == "None":
            decrypted = decompressed

        elif self.__data["encryption"] == "aes256":
            decrypted = self.__b64decode(AES256(self.__epass).decrypt(decompressed))

        else:
            raise ValueError("Invalid encryption algorithm name")

        """
        if type(decrypted) is bytes:
            decrypted = decrypted.decode()
        """

        if decrypted == "":
            # Another lazy check if plaintext is empty.
            self.__dictionary = {}
            return None

        # <variable_name>|<datatype>|<value>
        # <variable_name>|<datatype>|<array_datatype>|<values>
        self.__dictionary = json.loads(decrypted)

    def __writedict(self):
        """
        Replace existing data from self.__data["dictionary"] with <newdict>.

        :param str newdict: The whole dictionary to write.

        :returns void:
        """

        # Encrypt the result
        if self.__data["encryption"] == "None":
            eresult = self.__b64encode(json.dumps(self.__dictionary, separators=(',', ':')), True)

        elif self.__data["encryption"] == "aes256":
            eresult = self.__b64encode(AES256(self.__epass).encrypt(self.__b64encode(json.dumps(self.__dictionary, separators=(',', ':')))), True)

        else:
            raise ValueError("Invalid encryption algorithm name")

        # Compress the result
        if self.__data["compression"] == "None":
            cresult = eresult

        elif self.__data["compression"] == "zlib":
            cresult = zlib.compress(eresult)

        else:
            raise ValueError("Invalid compression algorithm name")

        self.__data["dictionary"] = self.__b64encode(cresult)

    def load(self, load_dict=True):
        """
        Get the current values of the configuration file.
        This method must be called first to work with the configuration file.

        :param bool load_dict: If True, this method will decrypt and decode the dictionary and store it to `self.__dictionary`.

        :returns void:
        """

        self.__readconfig()
        if load_dict:
            self.__readdict()

    def info(self):
        """
        Return information about the configuration file.

        :returns dict:
        """

        if self.__data is None:
            raise ValueError("The configuration file is not yet loaded!")

        result = self.__data
        try:
            result.pop("dictionary")

        except KeyError:
            pass

        if type(result["version"]) is not list and result["version"] is not None:
            newver = result["version"].split('.')

        else:
            newver = result["version"]

        # Convert result["version"] to a list of integers
        newver2 = []
        for _ in newver:
            newver2.append(int(_))

        result["version"] = newver2

        if self.__dictionary is None:
            result["loaded_dictionary"] = False

        else:
            result["loaded_dictionary"] = True

        return result

    def get(self, key):
        """
        Get the value of <key>.

        :param str key: The name/key of the value you are looking for.

        :returns str: Returns type(str) if the <key>'s datatype is `str`.
        :returns int: Returns type(int) if the <key>'s datatype is `int`.
        :returns float: Returns type(float) if the <key>'s datatype is `float`.
        :returns bool: Returns type(bool) if the <key>'s datatype is `bool`.
        :returns list: Returns type(list) if the <key>'s datatype is `arr`.
        :returns bytes: Returns type(bytes) if the <key>'s datatype is `bin`.
        """

        if self.__dictionary is None or self.__data is None:
            raise ValueError("The configuration file is not yet loaded!")

        elif type(self.__dictionary) is dict:
            value = self.__dictionary[key]
            if value[0] == "str":
                value = str(value[1])

            elif value[0] == "int":
                value = int(value[1])

            elif value[0] == "float":
                value = float(value[1])

            elif value[0] == "bool":
                if int(value[1]) == 0:
                    value = False

                elif int(value[1]) == 1:
                    value = True

                else:
                    raise ValueError("Unknown boolean state")

            elif value[0] == "arr":
                newvalue = value[2]
                valuearrdatatype = value[1]
                value = []
                for _ in newvalue:
                    if valuearrdatatype == "str":
                        value.append(str(_))

                    elif valuearrdatatype == "int":
                        value.append(int(_))

                    elif valuearrdatatype == "float":
                        value.append(float(_))

                    elif valuearrdatatype == "bool":
                        if int(_) == 0:
                            value.append(False)

                        elif int(_) == 1:
                            value.append(True)

                        else:
                            raise ValueError("Unknown boolean state")

                    elif valuearrdatatype == "bin":
                        value.append(self.__b64decode(_))

                    else:
                        raise ValueError("Invalid data type")

            elif value[0] == "bin":
                value = self.__b64decode(value[1])

            else:
                raise ValueError("Invalid data type")

            return value

        else:
            raise ValueError("Invalid dictionary")

    def add(self, key, valuetype, value, array_datatype=None):
        """
        Add a new variable.

        :param str key: The variable name/key.
        :param str valuetype: The data type of the variable.
                              Available valuetypes:
                                  - str
                                  - int
                                  - float
                                  - bool
                                  - arr (list)
                                  - bin (binary)

        :param str value: The value of <key>. (If <valuetype> is `str`)
        :param int value: The value of <key>. (If <valuetype> is `int`)
        :param float value: The value of <key>. (If <valuetype> is `float`)
        :param bool value: The value of <key>. (If <valuetype> is `bool`)
        :param tuple value: The value of <key>. (If <valuetype> is `arr`)
        :param list value: The value of <key>. (If <valuetype> is `arr`)
        :param bytes value: The value of <key>. (If <valuetype> is `bin`)

        :param str array_datatype: [OPTIONAL; If your valuetype is `arr`, this is required] The data type of the array objects (`arr` not supported)

        :returns void:
        """

        # <variable_name>|<datatype>|<value>
        # <variable_name>|<datatype>|<array_datatype>|<values>

        if type(key) is not str:
            raise TypeError("key is not a string")

        if self.__dictionary is None or self.__data is None:
            raise ValueError("The configuration file is not yet loaded!")

        if self.__dictionary.get(key, None) is None:
            # Add to the dictionary
            if valuetype in self.datatypes:
                if valuetype == "arr":
                    if array_datatype is None:
                        raise ValueError("array_datatype is required to create an array!")

                    keyvalue = [valuetype, array_datatype, []]
                    # Check the list
                    if type(value) in self.datatypes_conversion["arr"]:
                        for _ in value:
                            if keyvalue[1] == "str":
                                keyvalue[2].append(str(_))

                            elif keyvalue[1] == "int":
                                keyvalue[2].append(int(_))

                            elif keyvalue[1] == "float":
                                keyvalue[2].append(float(_))

                            elif keyvalue[1] == "bool":
                                if _ == True:
                                    keyvalue[2].append(1)

                                elif _ == False:
                                    keyvalue[2].append(0)

                                else:
                                    raise ValueError("Unknown boolean state")

                            elif keyvalue[1] == "bin":
                                if type(_) in self.datatypes_conversion["bin"]:
                                    keyvalue[2].append(self.__b64encode(_, True).decode(self.encoding))

                                else:
                                    raise("array object is not in bytes data type")

                            else:
                                raise ValueError("Unsupported array datatype")

                        self.__dictionary[key] = keyvalue

                    else:
                        raise TypeError("value must be a tuple or list when creating an array.")

                else:
                    if valuetype == "str":
                        self.__dictionary[key] = [valuetype, str(value)]

                    elif valuetype == "int":
                        self.__dictionary[key] = [valuetype, int(value)]

                    elif valuetype == "float":
                        self.__dictionary[key] = [valuetype, float(value)]

                    elif valuetype == "bool":
                        if value == True:
                            self.__dictionary[key] = [valuetype, 1]

                        elif value == False:
                            self.__dictionary[key] = [valuetype, 0]

                        else:
                            raise ValueError("Unknown boolean state")

                    elif valuetype == "bin":
                        if type(value) in self.datatypes_conversion["bin"]:
                            self.__dictionary[key] = [valuetype, self.__b64encode(value, True).decode(self.encoding)]

                        else:
                            raise ValueError("value is not in bytes data type")

                    else:
                        raise ValueError("Unsupported data type")

            else:
                raise ValueError("Unsupported data type")

        else:
            ValueError("A value is already assigned to the key. Use update() instead.")

    def update(self, key, value):
        """
        Update an existing variable.

        :param str key: The variable name/key to update.
        :param str value: The new value of <key>.

        :returns void:
        """

        # <variable_name>|<datatype>|<value>
        # <variable_name>|<datatype>|<array_datatype>|<values>

        if self.__dictionary is None or self.__data is None:
            raise ValueError("The configuration file is not yet loaded!")

        if self.__dictionary.get(key, None) is not None:
            if self.__dictionary[key][0] == "arr" and type(value) not in self.datatypes_conversion[self.__dictionary[key][0]]:
                raise TypeError("New value must be a list or a tuple")

            elif self.__dictionary[key][0] == "arr" and type(value) in self.datatypes_conversion[self.__dictionary[key][0]]:
                for _ in value:
                    if type(_) not in self.datatypes_conversion[self.__dictionary[key][1]]:
                        raise TypeError("New value has different datatype than the old value")

            if type(value) not in self.datatypes_conversion[self.__dictionary[key][0]]:
                raise TypeError("New value has different datatype than the old value")

            oldvalue = self.__dictionary[key]
            valuetype = oldvalue[0]
            # Add to the dictionary
            if valuetype == "arr":
                array_datatype = oldvalue[1]
                keyvalue = [valuetype, array_datatype, []]
                # Check the list
                if type(value) in self.datatypes_conversion[valuetype]:
                    for _ in value:
                        if keyvalue[1] == "str":
                            keyvalue[2].append(str(_))

                        elif keyvalue[1] == "int":
                            keyvalue[2].append(int(_))

                        elif keyvalue[1] == "float":
                            keyvalue[2].append(float(_))

                        elif keyvalue[1] == "bool":
                            if _ == True:
                                keyvalue[2].append(1)

                            elif _ == False:
                                keyvalue[2].append(0)

                            else:
                                raise ValueError("Unknown boolean state")

                        elif keyvalue[1] == "bin":
                            if type(_) in self.datatypes_conversion["bin"]:
                                keyvalue[2].append(self.__b64encode(_, True).decode(self.encoding))

                            else:
                                raise("array object is not in bytes data type")

                        else:
                            raise ValueError("Unsupported array datatype")

                    self.__dictionary[key] = keyvalue

                else:
                    raise TypeError("value must be a tuple or list when updating an array.")

            else:
                if valuetype == "str":
                    self.__dictionary[key] = [valuetype, str(value)]

                elif valuetype == "int":
                    self.__dictionary[key] = [valuetype, int(value)]

                elif valuetype == "float":
                    self.__dictionary[key] = [valuetype, float(value)]

                elif valuetype == "bool":
                    if value == True:
                        self.__dictionary[key] = [valuetype, 1]

                    elif value == False:
                        self.__dictionary[key] = [valuetype, 0]

                    else:
                        raise ValueError("Unknown boolean state")

                elif valuetype == "bin":
                    if type(value) in self.datatypes_conversion["bin"]:
                        self.__dictionary[key] = [valuetype, self.__b64encode(value, True).decode(self.encoding)]

                    else:
                        raise ValueError("value is not in bytes data type")

                else:
                    raise ValueError("Unsupported data type")

        else:
            ValueError("Key wasn't found in the dictionary")

    def remove(self, key):
        """
        Remove an existing variable.

        :param key: The key to remove.

        :returns void:
        """

        self.__dictionary.pop(key)

    def new(self, name, author=None, compression="None", encryption="None"):
        """
        Create a new configuration file.

        :param str name: The name of the configuration file.
        :param str author: [Optional] The name of the configuration file's author.
        :param str compression: The compression algorithm name (See self.compressions)
        :param str encryption: The encryption algorithm name (See self.encryptions)
        """

        if not os.path.exists(self.configpath):
            # Set the name
            self.__data["name"] = name

            # Set the author
            if author is None:
                self.__data["author"] = ""

            else:
                self.__data["author"] = author

            # The parser version is used as the config file version.
            # That way, we can drop support for older versions. (I hope we'll not do that)
            self.__data["version"] = self.VERSION

            # Set the compression
            if compression in self.compressions:
                self.__data["compression"] = compression

            else:
                raise ValueError("Unsupported compression algorithm name")

            # Set the encryption
            if encryption in self.encryptions:
                self.__data["encryption"] = encryption
                if (self.__epass is None and self.__data["encryption"] != "None") and type(self.__epass) not in (str, None):
                    raise ValueError("`epass` must be a string")

            else:
                raise ValueError("Unsupported encryption algorithm name")

            # Set the dictionary
            self.import_dict({})

            # Save the configuration file.
            self.save()

        else:
            raise FileExistsError("The configuration file is already present")

    def export_config(self):
        """
        Export the contents of the configuration file.

        :returns dict: The configuration file content.
        """

        if self.__data is None or self.__dictionary is None:
            raise ValueError("Dictionary is not yet loaded!")

        to_export = self.__data
        to_export["dictionary"] = self.__dictionary

        return to_export

    def import_dict(self, dictionary):
        """
        Overwrite the contents of the dictionary.

        :param dict dictionary: The new contents of the dictionary.

        :returns void:
        """

        # <variable_name>|<datatype>|<value>
        # <variable_name>|<datatype>|<array_datatype>|<values>

        for key in dictionary:
            # Check if object's datatype is supported
            if dictionary[key][0] in self.datatypes:
                # Check if object is an array
                if dictionary[key][0] == "arr":
                    # Check if array's datatype is supported
                    if dictionary[key][1] in self.array_datatypes:
                        # Check objects in array individually
                        for value in dictionary[key][2]:
                            if dictionary[key][1] == "bool":
                                if value in (0, 1):
                                    pass

                                else:
                                    raise ValueError("Unknown Boolean State")

                            elif dictionary[key][1] == "bin":
                                if self.__b64encode(self.__b64decode(value)) == value:
                                    pass

                                else:
                                    raise ValueError("Invalid binary data")

                            else:
                                if type(value) in self.array_datatypes_conversion[dictionary[key][1]]:
                                    pass

                                else:
                                    raise ValueError("An array object's datatype does not match the array's datatype")

                    else:
                        raise ValueError("Array datatype is not supported (see self.array_datatypes")

                else:
                    if dictionary[key][0] == "bool":
                        if dictionary[key][1] in (0, 1):
                            pass

                        else:
                            raise ValueError("Unknown boolean state")

                    elif dictionary[key][0] == "bin":
                        if self.__b64encode(self.__b64decode(dictionary[key][1])) == dictionary[key][1]:
                            pass

                        else:
                            raise ValueError("Invalid binary data")

                    else:
                        if type(dictionary[key][1]) in self.datatypes_conversion[dictionary[key][0]]:
                            pass

                        else:
                            raise ValueError("New dictionary has unsupported data type")

            else:
                raise ValueError("Unsupported datatype")

        self.__dictionary = dictionary

    def save(self):
        """
        Save the current data to <self.configpath>.

        :returns void:
        """

        self.__writedict()
        self.__writeconfig()
