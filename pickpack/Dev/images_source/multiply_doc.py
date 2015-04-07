
import os, shutil

dirpath = r'D:\Documents\Christian\Documents\Work\IA\Miller\Local projects\PickPack\Dev\Working Copy\Dev\images_source'
filename = 'battery_doc.svg'
filename_template = 'battery_doc%s.svg'
full_path_of_original = os.path.join(dirpath, filename)

for i in range (1,7):
    full_path_of_copy = os.path.join(dirpath, filename_template % i)
    #print full_path_of_copy
    shutil.copy(full_path_of_original,
                full_path_of_copy,
               )

print "Done"
