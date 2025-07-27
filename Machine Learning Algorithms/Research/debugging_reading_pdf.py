# testing: reading_pdf_contents_data_saver_with_concurrent.py

import time
from reading_pdf_contents_data_saver_with_concurrent import DocumentContentDataset

#Path = '/home/ngoni97/Documents/Python Programming'
#Path = '/home/ngoni97/Documents/PHYSICS'
Path = '/home/ngoni97/Documents/MATHEMATICS'

test = DocumentContentDataset(Path, pages=13, save_as_text_file=True)
# start
print('process in progress\n')
start = time.time()
test.returnData()
# end
end = time.time()
print('process complete\n')
    
print('time taken for execution = {}s'.format(round(end-start, 3)))

# sometimes it runs smoothly but other times not so well
