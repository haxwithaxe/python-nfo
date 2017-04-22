# Description
This library is intended to cover the XML NFO format as used by the Kodi project.

# To Do
* Parsing - currently only generates the XML.
* Fully implement all the complex node types.
* Movies, music video, etc support.

# Background
All I really wanted was to have hacker conference talks show up with some info in Kodi not just the filename.
Then I did one of these <https://xkcd.com/974/>. Now I can pass arbitrary NFO condiments.

# Reference
* <http://kodi.wiki/view/Video_management>
* <http://kodi.wiki/view/Naming_video_files/TV_shows>
* Export of my existing library

# Integration
This is how I did it. I don't know if it's the best way to do it.

## Files
All NFO files require an xml declaration. Without it the files won't be used by Kodi.

### tvshow.nfo
In the directory containing the all seasons of the TV show put the `tvshow.nfo` file with just the info for the TV show.
```
tv-show-title/
├── tv-show-title.season#
└── tvshow.nfo
```

#### Example tvshow.nfo
```
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<tvshow>
  <title>tv-show-title</title>
  <showtitle>tv-show-title/showtitle>
  <aired>1969-12-31</aired>
  <premiered>1969-12-31</premiered>
  <studio>production-studio</studio>
  <year>1969</year>
</tvshow>
```

### filename.nfo
Original filename with the extension replaced with `nfo`

Example:
```
ls .
showtitle-s01e01-episodetitle.mp4
showtitle-s01e01-episodetitle.nfo
```

The NFO file ?must? contain the following elements:
* showtitle - the title of the TV show.
* title - the title of the episode.
* episode - the episode number.
* season - season number.

### Renaming files
The video files need to be named in a way that the local data scraper. I have gone for the following pattern.
```
hello.showname/
└── hello.showname.01
	└── hello.showname-s01e01-hello.episodename.mp4
```

#### Not Renaming
To prevent the need for renaming files creating symlinks to the files that are not named appropriately works nicely.

### Importing
* <http://kodi.wiki/view/Set_content_and_scan>

1. Set the content type of the full TV show directory (eg `hello.tvshowname`) to `TV Show` and the scrapper to `local only`.
1. Wait for the scan to finish and everything will be displayed as expected.
