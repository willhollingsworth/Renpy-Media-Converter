# Renpy-Media-Converter

A Python toolkit for converting Ren'Py image sequences (with sound) into video files. Also updates the original code for easier implementation.


This is a work in progress and needs to be cleaned up quiet a lot.

## Features
- **Parse Ren'Py `.rpy` Files:** Extracts image sequence definitions and metadata from Ren'Py script files.
- **Image Sequence Validation:** Checks for issues such as inconsistent frame rates, unordered images, and missing repeats.
- **Audio Analysis:** Detects and processes associated audio, collecting metadata like position and duration.
- **Audio Processing:** Composes the audio files using collected metadata into a single file.
- **Automated Conversion:** Uses ffmpeg to convert image sequences and audio into webm video files.
- **Reporting:** Generates reports on animation tags, durations, and potential issues.
- **Ren'Py Code Generation:** Creates new `.rpy` files referencing the generated webm movies.

---

## Project Structure

```
renpy_media_converter/
│
├── renpy_media_converter/
│   ├── ffmpeg/           # ffmpeg integration for video processing
│   ├── rpy_reader/       # Reads and analyzes .rpy files
│   ├── rpy_writer/       # Writes new .rpy files for webm movies
│   ├── sound/            # Audio extraction and composition
│   ├── utils/            # Utilities: config, paths, file I/O
│   ├── main_logic.py     # Main orchestration logic
│   └── __init__.py
│
├── tests/                # Unit tests and test utilities
├── config.ini            # Configuration file for paths and settings
└── run.py                # Example entry point
```
---

## How It Works

1. **Configuration:**  
   Set up your `config.ini` with the correct paths for your Ren'Py game, images, audio, and output folders.

2. **Data Extraction:**  
   The tool parses `.rpy` files in your game folder to extract image sequence definitions and associated audio.

3. **Validation & Reporting:**  
   Image sequences are validated for potential issues (e.g., frame rate, image order, repeating sequence).

4. **Audio & Video Generation:**  
   - Audio segments are combined and timed using `pydub`.
   - Image sequences are converted to webm videos using ffmpeg, with audio tracks overlaid if present.

5. **Ren'Py Code Generation:**  
   New `.rpy` files are generated to reference the created webm movies, making it easier to integrate back into the project.

---

## Usage

1. **Install Dependencies:**
   - Python 3.8+
   - [pydub](https://github.com/jiaaro/pydub)
   - [ffmpeg](https://ffmpeg.org/) (ensure it's installed and the path is set in the code/config)
   - Pillow (for image analysis)

   Install Python dependencies:
   ```
   pip install pydub pillow
   ```

2. **Configure Paths:**
   Edit `config.ini` to match your project structure.

3. **Run the Main Script:**
   ```
   python run.py
   ```
   Or run individual modules for specific tasks.

---

## Key Modules

- **[main_logic.py](renpy_media_converter/main_logic.py):**  
  Orchestrates the full conversion pipeline.

- **[rpy_reader/rpy_reader.py](renpy_media_converter/rpy_reader/rpy_reader.py):**  
  Extracts and analyzes image sequences from `.rpy` files.

- **[sound/sound_creator.py](renpy_media_converter/sound/sound_creator.py):**  
  Combines and times audio segments for each animation.

- **[ffmpeg/create_video.py](renpy_media_converter/ffmpeg/create_video.py):**  
  Converts image sequences (and audio) into webm videos.

- **[rpy_writer/create_rpy.py](renpy_media_converter/rpy_writer/create_rpy.py):**  
  Generates new `.rpy` files referencing the created webm movies.

- **[utils/get_config.py](renpy_media_converter/utils/get_config.py):**  
  Loads and manages configuration settings.

---

## Customization & Extensibility

- **Add new validation rules** in `rpy_reader/categorizer.py`.
- **Adjust ffmpeg settings** in `ffmpeg/create_video.py` for different codecs or quality.
- **Extend reporting** in `rpy_reader/img_seq_report.py` for more analytics.

---

## Limitations & Notes

- Only `.jpg` images are currently supported for video conversion.
- Some features (e.g., handling of PNGs with alpha, audio that runs longer than the visuals) are not currently implemented
- Paths are currently Windows-style and will likely have issues on Mac/Linux.
- The code expects a specific Ren'Py project structure (see `config.ini`).

---

## Credits

- Uses [pydub](https://github.com/jiaaro/pydub) for audio processing.
- Uses [ffmpeg](https://ffmpeg.org/) for video encoding.