import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
from pytube import Playlist

class App:
    def __init__(self, root):
        #setting title
        root.title("YoutubeToIDM")
        #setting window size
        width = 604
        height = 55
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.playlist_entry = tk.Entry(root, borderwidth="1px")
        self.playlist_entry.place(x=10, y=10, width=353, height=30)

        self.download_button = tk.Button(root, bg="#f0f0f0", text="Download 720p Videos", command=self.download_videos)
        self.download_button.place(x=370, y=10, width=219, height=30)

    def extract_playlist_info(self, playlist_url):
        try:
            # Load playlist
            playlist = Playlist(playlist_url)

            # Extract information for each video
            videos_info = []
            for video in playlist.videos:
                video_info = {
                    "id": video.video_id,
                    "title": video.title,
                    "formats": video.streams.filter(progressive=True, file_extension='mp4').all()  # Filter for mp4 format
                }
                videos_info.append(video_info)

            return videos_info
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def save_to_file(self, video_info, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for video_info in video_info:
                    video_title = video_info["title"].replace(" ", "%20")
                    video_id = video_info["id"]
                    for fmt in video_info['formats']:
                        if fmt.resolution == "720p":
                            video_url = fmt.url  # Get the URL of the first available format
                            concatenated_info = f"{video_url}&title={video_title}"
                            f.write(concatenated_info + '\n')
                            break  # Break after finding 720p format
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving to file: {str(e)}")

    def download_videos(self):
        playlist_url = self.playlist_entry.get()
        if not playlist_url:
            messagebox.showwarning("Warning", "Please enter a playlist URL")
            return

        filename = "playlist.txt"

        videos_info = self.extract_playlist_info(playlist_url)
        if videos_info:
            self.save_to_file(videos_info, filename)
            messagebox.showinfo("Success", f"Playlist information saved to {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
