# Aiptasia GUI Notes

This directory contains files pertaining to a graphical user interface (GUI) for Pablo A. Curiel's aiptasia imaging work.

## Misc. notes
- Naming format for csv prompt files (w/o braces): {image basename}_{date_time}.csv
- Prompting CSV header format: file_name, prompt_id, point_x, point_y, is_pos, canvas_oval_id, aip_id 

## TODO
- Add undo/redo capability (stack/queue-based)
- Create modes for prompting, drawing/painting/editing predicted/GT masks, and predicting new masks
- Embed (finetuned SAM in the backend)
- Check if we need to load the PIL image in both the main app class and user action class (seems to be waste of memory)
- Store location of placed points
- Create ability to load in multiple images at a time
    - Only load in PIL image for image currently being viewed
    - Store filenames of other images
    - Possibly use toolbar on the left showing all image filenames
        - Display image when specific filename clicked
- Rewrite to make code more modular? 
- Determine where to store prompt points
    - Likely in own class
- Possibly a third prompt point for edge cases (i.e. overlapping aiptasia, etc.)
- ~~Make better use of branches~~
- ~~Sort ALL GUI code (scratch, test, main, etc.)~~
- ~~Track position of cursor on image by displaying image coordinates~~
- ~~Create ability to put points on image pixels that align with user actions (pan, zoom, etc.)~~
- ~~Use image pyramid for more efficient memory usage~~
- ~~Find out why image requires a user action to show up instead of showing when app opens~~
- ~~Set max panning such that image is always somewhat in frame~~