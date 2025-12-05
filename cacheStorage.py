import random

class CacheStorageSystem:
    def __init__(self, nominal_size: int, words_per_block: int, mapping_policy: int, blocks_per_set: int):
        
        bytes_per_word = 4
        self.block_size_bytes = words_per_block * bytes_per_word
        self.nominal_size = nominal_size * 1024
        
        # Calculate number of blocks
        self.num_blocks = self.nominal_size // self.block_size_bytes
        
        # Handle mapping policy
        self.mapping_policy = mapping_policy
        
        # mapping policy: 0 is direct, 1 is set associative

        if self.mapping_policy == 0:
            # Direct mapped: sets = blocks, associativity = 1
            self.num_sets = self.num_blocks
            self.associativity = 1
        elif self.mapping_policy == 1:
            # Set associative
            self.associativity = blocks_per_set
            self.num_sets = self.num_blocks // blocks_per_set
        else:
            raise ValueError("mapping_policy must be 'direct', 'set', or 'full'")
        
        # Calculate real size (including overhead)
        tag_bits_per_block = 32 - (self.block_size_bytes.bit_length() - 1) - (self.num_sets.bit_length() - 1 if self.num_sets > 1 else 0)
        valid_bit_overhead = 1
        total_overhead_bits = self.num_blocks * (tag_bits_per_block + valid_bit_overhead)
        total_data_bits = self.nominal_size * 8
        self.real_size_bytes = (total_data_bits + total_overhead_bits) // 8
        
        # Address partitioning (32-bit addresses)
        self.offset_bits = (self.block_size_bytes.bit_length() - 1)
        self.index_bits = (self.num_sets.bit_length() - 1) if self.num_sets > 1 else 0
        self.tag_bits = 32 - self.offset_bits - self.index_bits
        
        # Initialize cache state
        self.cache = [[{'tag': -1, 'valid': False} for _ in range(self.associativity)] 
                      for _ in range(self.num_sets)]
        
        # Access history and statistics
        self.access_history = []
        self.total_accesses = 0
        self.hits = 0
        self.misses = 0
        
        # For LRU replacement
        self.lru_counter = [[0 for _ in range(self.associativity)] for _ in range(self.num_sets)]
        self.time = 0
    
    def get_cache_info(self):
        """Return cache configuration information."""
        return {
            'num_blocks': self.num_blocks,
            'num_sets': self.num_sets,
            'mapping_policy': self.mapping_policy,
            'associativity': self.associativity,
            'words_per_block': self.block_size_bytes // 4,
            'block_size_bytes': self.block_size_bytes,
            'offset_bits': self.offset_bits,
            'index_bits': self.index_bits,
            'tag_bits': self.tag_bits,
            'nominal_size': self.nominal_size,
            'real_size_bytes': self.real_size_bytes,
            'address_partitioning': f"Tag:{self.tag_bits} bits, Index:{self.index_bits} bits, Offset:{self.offset_bits} bits"
        }
    
    def access_address(self, word_address):
        """Process a memory access and return hit/miss result."""
        self.total_accesses += 1
        self.time += 1
        
        # Convert to byte address (4 bytes per word)
        byte_addr = word_address * 4
        
        # Extract address parts
        offset = byte_addr & ((1 << self.offset_bits) - 1)
        index = (byte_addr >> self.offset_bits) & ((1 << self.index_bits) - 1)
        tag = byte_addr >> (self.offset_bits + self.index_bits)
        
        # Check for hit
        hit = False
        way = -1
        set_data = self.cache[index]
        
        for i in range(self.associativity):
            if set_data[i]['valid'] and set_data[i]['tag'] == tag:
                hit = True
                way = i
                self.hits += 1
                self.lru_counter[index][i] = self.time
                break
        
        if not hit:
            self.misses += 1
            
            # Find replacement way (LRU)
            lru_way = 0
            min_time = self.lru_counter[index][0]
            
            for i in range(1, self.associativity):
                if not set_data[i]['valid']:
                    lru_way = i
                    break
                if self.lru_counter[index][i] < min_time:
                    min_time = self.lru_counter[index][i]
                    lru_way = i
            
            # Replace
            self.cache[index][lru_way]['tag'] = tag
            self.cache[index][lru_way]['valid'] = True
            self.lru_counter[index][lru_way] = self.time
            way = lru_way
        
        # Record access
        access_record = {
            'address': word_address,
            'tag': tag,
            'index': index,
            'offset': offset,
            'hit': hit,
            'location': f"Set {index}, Way {way}"
        }
        self.access_history.append(access_record)
        
        return access_record
    
    def get_access_history(self):
        """Return the access history table."""
        return self.access_history
    
    def clear_cache(self):
        """Clear the cache and reset statistics."""
        self.cache = [[{'tag': -1, 'valid': False} for _ in range(self.associativity)] 
                      for _ in range(self.num_sets)]
        self.lru_counter = [[0 for _ in range(self.associativity)] for _ in range(self.num_sets)]
        self.access_history = []
        self.total_accesses = 0
        self.hits = 0
        self.misses = 0
        self.time = 0
    
    def simulation(self, num_accesses=1000, address_range=(0, 1024)):
        """Run a simulation with random addresses."""
        # Clear for fresh simulation
        self.clear_cache()
        
        min_addr, max_addr = address_range
        
        for _ in range(num_accesses):
            # Generate address with some locality
            if random.random() < 0.7 and self.access_history:
                last_addr = self.access_history[-1]['address']
                addr = last_addr + random.randint(-10, 10)
                addr = max(min_addr, min(addr, max_addr))
            else:
                addr = random.randint(min_addr, max_addr)
            
            self.access_address(addr)
        
        # Calculate hit rate
        hit_rate = (self.hits / num_accesses * 100) if num_accesses > 0 else 0
        
        return {
            'total_accesses': num_accesses,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'miss_rate': 100 - hit_rate
        }