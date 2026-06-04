#!/usr/bin/env python3

import dataclasses

@dataclasses.dataclass
class DownloadInfo:
    version: str
    tarball: int
    linux: int
    macos: int

downloads = (
    DownloadInfo(version="v4.2.1", tarball=47, linux=233, macos=6+63),
    DownloadInfo(version="v4.2.0", tarball=49, linux=403, macos=104+105),
    DownloadInfo(version="v4.1.3", tarball=69, linux=326, macos=70+42),
    DownloadInfo(version="v4.0.0", tarball=76, linux=227, macos=83+70),
    DownloadInfo(version="v3.0.3", tarball=99, linux=592, macos=148+77),
    DownloadInfo(version="v3.0.1", tarball=46, linux=173, macos=89),
    DownloadInfo(version="v3.0.0", tarball=94, linux=78, macos=69),
    DownloadInfo(version="v2.2.2", tarball=661, linux=545, macos=2143),
    DownloadInfo(version="v2.2.1", tarball=413, linux=1123+239, macos=610),
    DownloadInfo(version="v2.2.0", tarball=264, linux=230+555, macos=342),
)

cumulative = 0
for download in downloads:
    download_total = download.tarball + download.linux + download.macos
    print(f"{download.version}  {download_total}")
    cumulative += download_total

print(f"{cumulative} total downloads across {len(downloads)} versions")
