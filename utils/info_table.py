''' create a table that stores info in the format <key> - <legend> '''


class InfoTable:
    ''' create a table that stores info in the format <key> - <legend> '''
    def __init__(self):
        self._array = []
        self._max_key_len = 0
        self._max_value_len = 0

    def append(self, key, value):
        ''' add key-value pair to the end of the array '''
        self._measure_key_value(key=key, value=value)
        self._array.append({'key': key, 'value': value})

    def pop(self, index: int):
        ''' remove key-value pair from the array '''
        return self._array.pop(index)


    def get(self, index: int):
        ''' returns the key-value pair at the index specified '''
        return self._array[index]

    def get_key(self, index: int):
        ''' returns the key at the index specified '''
        return self._array[index]['key']

    def get_value(self, index: int):
        ''' returns the value at the index specified '''
        return self._array[index]['value']


    def set(self, index: int, key, value):
        ''' set the key-value pair at the index specified '''
        self._measure_key_value(key=key, value=value)
        self._array[index] = {'key': key, 'value': value}

    def set_key(self, index: int, key):
        ''' set the key at the index specified '''
        self._measure_key_value(key=key)
        self._array[index]['key'] = key

    def set_value(self, index: int, value:  str):
        ''' set the value at the index specified '''
        self._measure_key_value(value=value)
        self._array[index]['value'] = value


    def clear(self):
        ''' resets table '''
        self._array = []
        self._max_key_len = 0
        self._max_value_len = 0


    @property
    def max_key_len(self):
        ''' returns the length of the longest key in the table'''
        return self._max_key_len

    @property
    def max_value_len(self):
        ''' returns the length of the longest value in the table'''
        return self._max_value_len

    def _measure_key_value(self, key=None, value=None):
        try:
            key = key.get()
        except AttributeError:
            pass

        try:
            value = value.get()
        except AttributeError:
            pass

        if len(str(key)) > self._max_key_len:
            self._max_key_len = len(str(key))

        if len(str(value)) > self._max_value_len:
            self._max_value_len = len(str(value))

    def __iter__(self):
        for item in self._array:
            yield item

    def __len__(self):
        return len(self._array)
