from cacheStorage import *

def get_values():
    # get the nominal size of the cache in bytes
    while(True):
        nominal_size = input("Give nominal size in bytes: ")
        try:
            nominal_num = int(nominal_size)
            break
        except ValueError:
            print("Invalid input, try again!")

    # get the number of words per block in the cache, must be 1, 2, 4, or 8
    while(True):
        words_per_block = input("Give the number of words per block (1,2,4,8): ")
        try:
            words_per_block_num = int(words_per_block)
            if(not words_per_block_num in (1, 2, 4, 8)):
                print("invalid input, try again!")
            else:
                break
        except ValueError:
            print("invalid input, try again!")

    # get the mapping police of the cache
    # mapping policy key: 0 for Direct-Mapped, 1 for Set-Associative
    while(True):
        mapping_policy = input("Enter mapping policy, 0 for Direct-Mapped and 1 for set-associative: ")
        if(mapping_policy == "1"):
            # if set-associative...

            # get the number of blocks per set
            while(True):
                blocks_per_set = input("Give the number of blocks per set: ")
                try:
                    blocks_per_set_num = int(blocks_per_set)
                    break
                except ValueError:
                    print("Invalid input, try again!")

            break
        elif(mapping_policy == "0"):
            # if direct mapped set unused values to null (None)
            blocks_per_set_num = None
            break
        else:
            print("Invalid input! Try again")

    #return all the values
    return nominal_num, words_per_block_num, int(mapping_policy), blocks_per_set_num

def main():
    nominal_size, words_per_block, mapping_policy_int, blocks_per_set = get_values()
    cache = CacheStorageSystem(nominal_size, words_per_block, mapping_policy_int, blocks_per_set)
    cache_info = cache.get_cache_info()
    print(cache_info)

if __name__ == "__main__":
    main()