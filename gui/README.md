# Aiptasia GUI Notes

## TODO
- ~~Find out why image requires a user action to show up instead of showing when app opens~~
- Set max panning such that image is always somewhat in frame
- Check if we need to load the PIL image in both the main app class and user action class (seems to be waste of memory)
- Create ability to put points on image pixels that align with user actions (pan, zoom, etc.)
- Store location of placed points
- Track position of cursor on image by displaying image coordinates
- Create ability to load in multiple images at a time
    - Only load in PIL image for image currently being viewed
    - Store filenames of other images
    - Possibly use toolbar on the left showing all image filenames
        - Display image when specific filename clicked
        