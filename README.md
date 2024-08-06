# Video Merge Script

This Python script processes and merges video files from a specified directory. It handles video rotation and scaling, then concatenates the processed videos into a single output file.

## Features

- Retrieves and applies video rotation metadata.
- Scales videos to 1280x720 while preserving aspect ratio.
- Concatenates multiple video files into a single output file.
- Deletes temporary files after processing.

## Requirements

- Python 3.12.0
- ffmpeg version 7.0.1
- ffprobe version 7.0.1

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Ensure `ffmpeg` and `ffprobe` are installed:**

   You can download and install `ffmpeg` from [FFmpeg's official website](https://ffmpeg.org/download.html).

   To verify the installation, run:

   ```bash
   ffmpeg -version
   ffprobe -version
   ```

## Configuration

1. **Create a configuration file `config.json` in the project directory with the following structure:**

   ```json
   {
     "input_directory": "path/to/your/input/directory",
     "output_file": "path/to/your/output/file/output.mp4",
     "allowed_extensions": [".mp4", ".mov", ".avi"]
   }
   ```

   - `input_directory`: Directory containing the video files to be processed.
   - `output_file`: Path and name of the output video file.
   - `allowed_extensions`: List of video file extensions to include.

## Usage

1. **Run the script:**

   ```bash
   python merge_videos.py --verbose
   ```

   - `--verbose` (optional): Increases output verbosity, showing detailed processing steps.

## Script Overview

### `merge_videos.py`

- **get_video_rotation(filename)**: Retrieves the rotation metadata of a video file.
- **process_video(input_file, output_file, rotation, verbose)**: Processes a video file (rotation and scaling) and saves it as a temporary file.
- **gather_video_files(input_directory, allowed_extensions, verbose)**: Collects and sorts video files from the specified directory.
- **create_temp_files(video_files, verbose)**: Processes video files and creates temporary files.
- **create_filelist(temp_files, verbose)**: Creates `filelist.txt` containing paths to the temporary files.
- **concatenate_videos(output_file, verbose)**: Concatenates temporary files into the final output file.
- **clean_up(temp_files, verbose)**: Deletes temporary files and `filelist.txt`.
- **main(verbose)**: Main function that orchestrates the entire video merging process.

## Example

1. **Configuration (`config.json`):**

   ```json
   {
     "input_directory": "videos",
     "output_file": "output/merged_video.mp4",
     "allowed_extensions": [".mp4", ".mov"]
   }
   ```

2. **Directory Structure:**

   ```
   .
   ├── videos
   │   ├── video1.mp4
   │   ├── video2.mov
   │   └── video3.mp4
   ├── output
   │   └── merged_video.mp4
   ├── config.json
   ├── merge_videos.py
   ├── requirements.txt
   └── README.md
   ```

3. **Running the script:**

   ```bash
   python merge_videos.py --verbose
   ```

   The output video will be saved as `output/merged_video.mp4`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
