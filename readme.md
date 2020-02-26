# Python parallel downloader

## Usage

downloader=parallel_downloader.ParallelDownloader(number_of_worker_threads=4)

downloader.append("URL","local file name")#as many as you want

downloader.start()#blocking method

That's all for now.
