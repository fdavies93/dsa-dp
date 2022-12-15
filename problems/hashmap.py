# framework for hashmap class using only more basic structures

# you can use the hash() function to generate a hash value from a key for indexing
# bucket_index = hash(key) % len(self.buckets)

class Hashmap:
    def __init__(self,length):
        self.buckets = [None] * length
    
    def set_val(self, key, obj):
        bucket_index = hash(key) % len(self.buckets)
        # if bucket is empty, create a new one and assign the value 
        # if key already exists in bucket, change its value
        # if the bucket exists but it's not in the bucket, add it to the bucket

    def remove(self, key):
        bucket_index = hash(key) % len(self.buckets)
        # if no bucket corresponding to key found, throw an error or return None
        # find and delete the entry in the bucket with the correct key
        # edge case: this key collides but isn't actually in the bucket
        # if length of bucket is 0, reset the bucket to None

    def get(self, key):
        bucket_index = hash(key) % len(self.buckets)
        # if no bucket found, return None
        # if key found in bucket, return value
        # if no key found in bucket (false collision), return None

    def keys(self):
        key_list = []
        # construct and return a list of keys

    def values(self):
        val_list = []
        # construct and return a list of values

to_add = [ ("Tony", 23400), ("Percy", 30000), ("Rich", 100000), ("Billy", 40000) ]
hm = Hashmap(25)
for entry in to_add:
    hm.set_val(entry[0], entry[1])

print(hm.buckets)
print(hm.get("Percy"))
print(hm.keys())
print(hm.values())