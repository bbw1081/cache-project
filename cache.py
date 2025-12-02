
nominal_size = input("Give nominal size in bytes ")

words_per_block = input("Give the number of words per block (1,2,4,8)")
while(true):
    if(not words_per_block in (1, 2, 4, 8)):
        words_per_block = input("Try again! must be 1, 2, 4, or 8")
    else:
        break

# maping policy : 0 for DM, 1 for set-associative
while(True):
    mapping_policy = input("Enter mapping policy, 0 for Direct-Mapped and 1 for set-associative ")
    if(mapping_policy == "1"):
        n_sets = input("enter the N number of sets ")
        break
    elif(mapping_policy == "0"):
        break
    else:
        print("Invalid input! Try again")

        