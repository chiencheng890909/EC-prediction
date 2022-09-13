train_path = "train/image"
train_data_path = "train/text"

test_path = "test/image"
test_data_path = "test/text"

#train data (text)
train_data = list.files(file.path(getwd(), train_path))
for (i in 1:length(train_data)) {
  file = read.table(file.path(train_path, train_data[i]), comment="", header=FALSE)
  write.table(file, file.path(train_data_path, train_data[i]), sep=",", col.names=FALSE, row.names=FALSE)
}

#test data (text)
test_data = list.files(file.path(getwd(), test_path))
for (i in 1:length(test_data)) {
  file = read.table(file.path(test_path, test_data[i]), comment="", header=FALSE)
  write.table(file, file.path(test_data_path, test_data[i]), sep=",", col.names=FALSE, row.names=FALSE)
}
