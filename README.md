# GitHub-ForceLargeFiles

This package is a simple work around for pushing large files to a GitHub repo.


Since GitHub only allows pushing files up to 100 MB, a different service (such as [LFS](https://git-lfs.github.com/)) has to be used for larger files. This package compresses and splits large files that can be pushed to a GitHub repo without LFS. 

It starts off at a root directory and traverses down subdirectories, and scans every file contained. If any file has a size that is above `threshold_size`, then they are compressed and split to multiple archives, each having a maximum size of `partition_size`. Compressing/Splitting works for any file extension. 

After compression/split, files can be pushed the usual way, using `git push`.


## Parallelization
- Although traversing directories in `src/main.py` is serial, compressing/splitting each file through 7z is parallelized by default.
- Reversing with `src/reverse.py` is entirely serial. (TODO: Parallelize this too)


## Requirements
- Python 3.x.x. 
- You need to have 7z installed. Visit the [7z Download](https://www.7-zip.org/download.html) page for more information.
- Folders/Files in the traversed directories should have appropriate read/write permissions.


## Example Usage
Run with the default parameters:

```
$ python3 src/main.py  --root_dir ~/MyFolder
```
which will traverse down every subdirectory starting from `~/MyFolder`, and reduce all files over 100 MB to smaller archives with maximum size of approximately 95 MB. The default option is to delete the original (large) files afterwards, but this can be turned off.

The comparison below describes the use of this package more clearly.

Before:
```
$ tree --du -h ~/MyFolder

└── [415M]  My Datasets
│   ├── [6.3K]  Readme.txt
│   └── [415M]  Data on Leaf-Tailed Gecko
│       ├── [ 35M]  DatasetA.zip
│       ├── [ 90M]  DatasetB.zip
│       ├── [130M]  DatasetC.zip
│       └── [160M]  Books
│           ├── [ 15M]  RegularBook.pdf
│           └── [145M]  BookWithPictures.pdf
└── [818M]  Video Conference Meetings
    ├── [817M]  Discussion_on_Fermi_Paradox.mp4
    └── [1.1M]  Notes_on_Discussion.pdf
```

After:

```
$ tree --du -h ~/MyFolder

└── [371M]  My Datasets
│   ├── [6.3K]  Readme.txt
│   └── [371M]  Data on Leaf-Tailed Gecko
│       ├── [ 35M]  DatasetA.zip
│       ├── [ 90M]  DatasetB.zip
│       ├── [ 95M]  DatasetC.zip.7z.001
│       ├── [ 18M]  DatasetC.zip.7z.002
│       └── [133M]  Books
│           ├── [ 15M]  RegularBook.pdf
│           ├── [ 95M]  BookWithPictures.pdf.7z.001
│           └── [ 23M]  BookWithPictures.pdf.7z.002
└── [794M]  Video Conference Meetings
    ├── [ 95M]  Discussion_on_Fermi_Paradox.mp4.7z.001
    ├── [ 95M]  Discussion_on_Fermi_Paradox.mp4.7z.002
    ├── [ 95M]  Discussion_on_Fermi_Paradox.mp4.7z.003
    ├── [ 95M]  Discussion_on_Fermi_Paradox.mp4.7z.004
    ├── [ 95M]  Discussion_on_Fermi_Paradox.mp4.7z.005
    ├── [ 95M]  Discussion_on_Fermi_Paradox.mp4.7z.006
    ├── [ 95M]  Discussion_on_Fermi_Paradox.mp4.7z.007
    ├── [ 95M]  Discussion_on_Fermi_Paradox.mp4.7z.008
    ├── [ 33M]  Discussion_on_Fermi_Paradox.mp4.7z.009
    └── [1.1M]  Notes_on_Discussion.pdf
```
To revert back to the original files, run:
```
$ python3 src/reverse.py  --root_dir ~/MyFolder
``` 
