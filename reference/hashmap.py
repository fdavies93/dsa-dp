class Hashmap:
    def __init__(self,length):
        self.buckets = [None] * length
    
    def set_val(self, key, obj):
        # empty bucket
        bucket_index = hash(key) % len(self.buckets)
        if self.buckets[bucket_index] == None:
            self.buckets[bucket_index] = [(key, obj)]
            return
        
        # key already exists in bucket
        for entry in self.buckets[bucket_index]:
            if key == entry[0]:
                entry[1] = obj
                return

        # collision, but key doesn't exist
        self.buckets[bucket_index].append((key,obj))

    def remove(self, key):
        bucket_index = hash(key) % len(self.buckets)
        if self.buckets[bucket_index] == None:
            return

        for i, entry in enumerate(self.buckets[bucket_index]):
            if entry[0] == key:
                to_remove = i
                break
        
        del self.buckets[bucket_index][i]

        if len(self.buckets[bucket_index]) == 0:
            self.buckets[bucket_index] = None

    def get(self, key):
        bucket_index = hash(key) % len(self.buckets)

        if self.buckets[bucket_index] == None:
            return None

        for entry in self.buckets[bucket_index]:
            if entry[0] == key:
                return entry[1]
        
        return None

    def keys(self):
        key_list = []
        for bucket in self.buckets:
            if bucket == None:
                continue
            for entry in bucket:
                key_list.append(entry[0])
        return key_list

    def values(self):
        val_list = []
        for bucket in self.buckets:
            if bucket == None:
                continue
            for entry in bucket:
                val_list.append(entry[1])
        return val_list

to_add = [ ("Tony", 23400), ("Percy", 30000), ("Rich", 100000), ("Billy", 40000) ]
hm = Hashmap(25)
for entry in to_add:
    hm.set_val(entry[0], entry[1])

print(hm.get("Tony"))