# int: Minimum number of n-grams occurence to be retained
# All Ngrams that occur less than n times are removed
# default value: 0

ngram_min_to_be_retained = 0

# real: Minimum ratio n-grams to skip
# (will be chosen among the ones that occur rarely)
# expressed as a ratio of the cumulated histogram
# default value: 0

ngram_min_rejected_ratio = 0

# NB: the n-gram skipping will go on until:
# ( minimal_ngram_count < ngram_min_to_be_retained ) OR ( rejected_ratio <= ngram_min_rejected_ratio)


# int: the 'n' of 'n'-gram
# default value: 2

gram_size = 3


# File containing the textual data to convert
# Image in file_name*.img
# Image in file_name*.txt
# Output will be :
#   file_name*.onehot
#   file_name*.ngram
#   file_name*.info

files_path = '/u/lisa/db/babyAI/textual_v2'

file_name_train_amat = 'BABYAI_gray_4obj_64x64.train.img'
file_name_valid_amat = 'BABYAI_gray_4obj_64x64.valid.img'
file_name_test_amat  = 'BABYAI_gray_4obj_64x64.test.img'
image_size = 32*32


# Use empty string if no dataset
file_name_train_img = 'BABYAI_gray_4obj_64x64.train.img'
file_name_valid_img = 'BABYAI_gray_4obj_64x64.valid.img'
file_name_test_img  = 'BABYAI_gray_4obj_64x64.test.img'

file_name_train_txt = 'BABYAI_gray_4obj_64x64.color-size-location-shape.train.txt'
file_name_valid_txt = 'BABYAI_gray_4obj_64x64.color-size-location-shape.valid.txt'
file_name_test_txt  = 'BABYAI_gray_4obj_64x64.color-size-location-shape.test.txt'

file_name_train_out = 'BABYAI_gray_4obj_64x64.color-size-location-shape.train'
file_name_valid_out = 'BABYAI_gray_4obj_64x64.color-size-location-shape.valid'
file_name_test_out  = 'BABYAI_gray_4obj_64x64.color-size-location-shape.test'

# None or a file '*.info'
file_info = None # 'BABYAI_gray_4obj_64x64.color-size-location-shape.train.info'
