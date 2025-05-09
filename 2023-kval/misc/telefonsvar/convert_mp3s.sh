rm wavs/*
for full_path in original_mp3s/*
do
filename_with_path=${full_path%.mp3}
filename=${filename_with_path##*/}
echo "$full_path"
ffmpeg -i "$full_path" -vn -acodec pcm_s16le -ac 1 -ar 16000 -f wav "wavs/$filename.wav"
done