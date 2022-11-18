import os

# Creating a list of filenames from working directory
cwd = os.getcwd()
dir_list = os.listdir(cwd)
print(dir_list)
  
# Open file3 in write mode
with open('mergedBooks.txt', 'w', encoding="utf-8") as outfile:
  
    # Iterate through list
    for names in dir_list[:-1]:
        
        # Open each file in read mode
        with open(names, encoding="utf8") as infile:
  
            # read the data from file1 and
            # file2 and write it in file3
            outfile.write(infile.read())
  
        # Add '\n' to enter data of file2
        # from next line
        outfile.write("\n")