# combine all files that suffix with .en into one file under a directory

dir=/home/cl/chenliang/Off-Target-MNMT/example_corpus/opus_dev_tokenized
target_file=/home/cl/chenliang/Off-Target-MNMT/example_corpus/opus_dev_tokenized/opus_dev.en.all

for file in $dir/*.en; do
    cat $file >> $target_file
done