import os
import argparse
import ffmpeg
import openai

def extract_audio(video_path, audio_path):
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, ac=1, ar='16000')
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Error extracting audio: {e}")

def transcribe_audio(audio_path):
    try:
        with open(audio_path, 'rb') as audio_file:
            response = openai.Audio.transcribe("whisper-1", audio_file)
        return response['text']
    except Exception as e:
        raise RuntimeError(f"Error transcribing audio: {e}")

def translate_text(text, target_languages):
    translations = {}
    for lang in target_languages:
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Translate the following text to {lang}: {text}",
                max_tokens=1000
            )
            translations[lang] = response['choices'][0]['text'].strip()
        except Exception as e:
            raise RuntimeError(f"Error translating to {lang}: {e}")
    return translations

def save_captions(captions, output_path, format):
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            if format == 'srt':
                for i, caption in enumerate(captions, start=1):
                    f.write(f"{i}\n00:00:{i:02},000 --> 00:00:{i+1:02},000\n{caption}\n\n")
            elif format == 'vtt':
                f.write("WEBVTT\n\n")
                for i, caption in enumerate(captions, start=1):
                    f.write(f"00:00:{i:02}.000 --> 00:00:{i+1:02}.000\n{caption}\n\n")
            else:
                raise ValueError("Unsupported format. Use 'srt' or 'vtt'.")
    except Exception as e:
        raise RuntimeError(f"Error saving captions: {e}")

def main():
    parser = argparse.ArgumentParser(description="AI Video Captioner: Generate captions for video files.")
    parser.add_argument('--video', required=True, help="Path to the input video file.")
    parser.add_argument('--lang', help="Comma-separated list of language codes for translation.")
    parser.add_argument('--output', required=True, help="Path to the output caption file.")
    parser.add_argument('--format', choices=['srt', 'vtt'], default='srt', help="Output caption format (default: srt).")

    args = parser.parse_args()

    video_path = args.video
    output_path = args.output
    format = args.format
    target_languages = args.lang.split(',') if args.lang else []

    audio_path = "temp_audio.wav"

    try:
        extract_audio(video_path, audio_path)
        transcription = transcribe_audio(audio_path)

        captions = [transcription]
        if target_languages:
            translations = translate_text(transcription, target_languages)
            captions.extend(translations.values())

        save_captions(captions, output_path, format)
        print(f"Captions saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

if __name__ == "__main__":
    main()
