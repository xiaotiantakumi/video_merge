import os
import json
import argparse
import subprocess

def get_video_rotation(filename):
    """Obtains rotation information for video files."""
    cmd = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
        'stream=side_data_list', '-of', 'default=noprint_wrappers=1:nokey=1', filename
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip()
    
    if 'rotation' in output:
        rotation_line = [line for line in output.split('\n') if 'rotation' in line]
        if rotation_line:
            return int(rotation_line[0].split('=')[1])
    
    return 0

def process_video(input_file, output_file, rotation, verbose):
    """Pre-processes (rotates and scales) a video file and saves it as a temporary file."""
    filter_cmd = "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2"
    
    if rotation == 90:
        filter_cmd = f"transpose=1,{filter_cmd}"
    elif rotation == 180:
        filter_cmd = f"transpose=2,transpose=2,{filter_cmd}"
    elif rotation == 270:
        filter_cmd = f"transpose=2,{filter_cmd}"
    
    cmd = [
        'ffmpeg', '-i', input_file, '-vf', filter_cmd, '-c:v', 'libx264', '-crf', '23', 
        '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '192k', '-strict', 'experimental', output_file
    ]
    
    if verbose:
        print("Running command:", " ".join(cmd))
    
    subprocess.run(cmd)

def gather_video_files(input_directory, allowed_extensions, verbose):
    """Collects video files from the specified directory and sorts them by modification date."""
    video_files = []
    
    for root, _, files in os.walk(input_directory):
        for file in files:
            if any(file.endswith(ext) for ext in allowed_extensions):
                file_path = os.path.join(root, file)
                video_files.append(file_path)
                if verbose:
                    print(f"Found video file: {file_path}")
    
    video_files.sort(key=lambda x: os.path.getctime(x), reverse=True)
    
    if verbose:
        print("Sorted video files:")
        for video_file in video_files:
            print(video_file)
    
    return video_files

def create_temp_files(video_files, verbose):
    """Preprocesses video files and creates temporary files."""
    temp_files = []
    
    for index, video_file in enumerate(video_files):
        rotation = get_video_rotation(video_file)
        temp_file = f"temp_{index}.mp4"
        process_video(video_file, temp_file, rotation, verbose)
        temp_files.append(temp_file)
    
    return temp_files

def create_filelist(temp_files, verbose):
    """Create a filelist.txt file."""
    with open('filelist.txt', 'w') as filelist:
        for temp_file in temp_files:
            filelist.write(f"file '{temp_file}'\n")
    
    if verbose:
        print("Created filelist.txt with the following entries:")
        with open('filelist.txt', 'r') as filelist:
            print(filelist.read())

def concatenate_videos(output_file, verbose):
    """Combine temporary files to create final output."""
    cmd = [
        'ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'filelist.txt', '-c', 'copy', output_file
    ]
    
    if verbose:
        print("Running command:", " ".join(cmd))
    
    subprocess.run(cmd)

def clean_up(temp_files, verbose):
    """Delete temporary files and filelist.txt."""
    for temp_file in temp_files:
        os.remove(temp_file)
    
    os.remove('filelist.txt')
    
    if verbose:
        print("Cleaned up temporary files and filelist.txt.")

def main(verbose):
    """Main Processing. Reads the configuration file, preprocesses and combines video files."""
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    input_directory = config['input_directory']
    output_file = config['output_file']
    allowed_extensions = config['allowed_extensions']

    video_files = gather_video_files(input_directory, allowed_extensions, verbose)
    temp_files = create_temp_files(video_files, verbose)
    create_filelist(temp_files, verbose)
    concatenate_videos(output_file, verbose)
    clean_up(temp_files, verbose)

    if verbose:
        print(f"Output video saved as: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge videos from a directory based on metadata.")
    parser.add_argument('--verbose', action='store_true', help="Increase output verbosity")
    args = parser.parse_args()
    main(args.verbose)
