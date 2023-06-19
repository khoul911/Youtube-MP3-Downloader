import os, time, re
from pytube import YouTube, Playlist
from pytube.cli import on_progress

desktop_path = os.environ["USERPROFILE"] + "/Desktop/test/"
outtmpl = desktop_path + "/%(title)s.%(ext)s"


def save_path():
	destination = str(input("\nEnter the save path (leave blank to save in Desktop): "))
	if len(destination) < 3:
		destination = desktop_path
	return destination

def get_youtube_url():
	while True:
		clear_terminal()
		url =str(input("\nEnter a Youtube URL: "))
		if url.startswith('https://www.youtube.com/'):
			return url
		else:
			print("\nError: A valid url was not provided.\n")
			time.sleep(1.5)
		

def download_single_video():
	url = get_youtube_url()
	video = YouTube(url, on_progress_callback=on_progress)
	
	destination = save_path()

	video_author = video.author
	video_author = re.sub("[^a-zA-Z0-9 \n\.]", "", video_author)

	video_title = video.title
	video_title = re.sub("[^a-zA-Z0-9 \n\.]", "-", video_title)

	base_name = video_author + " - " + video_title + ".mp3"
	final_file_path = destination + base_name
	
	clear_terminal()
	print("\nDownloading -- " + base_name + "...")
	
	if os.path.isfile(final_file_path):
		time.sleep(1)
		print("\nError: File -- " + base_name + " -- already exists.\n")
		return

	try:
		yt = video.streams.filter(only_audio=True).first()
	except:
		time.sleep(1)
		print("Error: File -- " + base_name + " -- was not downloaded.\n")
		return

	try:
		yt.download(output_path=destination, filename=base_name)
		print("Success: File -- " + base_name + " -- was downloaded.\n")
	except:
		time.sleep(1)
		print("Error: File -- " + base_name + " -- was not downloaded.\n")
		print("\n")
		return


def download_playlist():
	url = get_youtube_url()
	playlist = Playlist(url)
	video_count = len(playlist.video_urls)
	print("\nNumber of videos found in the playlist: " + str(video_count) + "\n")

	destination = save_path()

	clear_terminal()
	print("\nDownloading, please wait...\n")
	count = 0
	count_error = 0
	start_time = time.time()

	for video in playlist.videos:
		video.register_on_progress_callback(on_progress)
		video_author = video.author
		video_author = re.sub("[^a-zA-Z0-9 \n\.]", "", video_author)

		video_title = video.title
		video_title = re.sub("[^a-zA-Z0-9 \n\.]", "-", video_title)

		base_name = video_author + " - " + video_title + ".mp3"

		final_file_path = destination + base_name

		print("\nDownloading -- " + base_name + "...")
		if os.path.isfile(final_file_path):
			print("\nError: File -- " + base_name + " -- already exists.\n")
			count_error+=1
			continue

		try:
			yt = video.streams.filter(only_audio=True).first()
		except:
			count_error+=1
			continue

		try:
			yt.download(output_path=destination, filename=base_name)
			count += 1
		except:
			print("Error: File -- " + base_name + " -- was not downloaded.\n")
			count_error+=1
		print("\n")

	end_time = time.time() - start_time
	print(str(count) + " files downloaded.\n")
	print(str(count_error) + " files not downloaded.\n")
	print(f"Total time spent: {str(end_time)} seconds.\n")


def clear_terminal():
	os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
	clear_terminal()
	while True:
		clear_terminal()
		print("Do you want to download:\n")
		print("[1] Single Video\n")
		print("[2] Playlist\n\n")
		download_option = input("Select an option: ")
		if download_option == "1":
			download_single_video()
			break
		elif download_option == "2":
			download_playlist()
			break
		else:
			print(
				"\nError: A valid option was not selected, please select a valid option.\n\n"
			)
			time.sleep(2)
