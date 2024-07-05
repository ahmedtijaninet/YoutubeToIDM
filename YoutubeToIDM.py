import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.font as tkFont
from pytube import Playlist

class App:
    def __init__(self, root):
        root.title("YoutubeToIDM")
        width = 604
        height = 300
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.playlist_entry = tk.Entry(root, borderwidth="1px")
        self.playlist_entry.place(x=10, y=10, width=353, height=30)

        self.quality_var = tk.StringVar(value="720p")
        self.quality_menu = ttk.Combobox(root, textvariable=self.quality_var, values=["360p", "480p", "720p", "1080p"])
        self.quality_menu.place(x=370, y=10, width=100, height=30)

        self.download_button = tk.Button(root, bg="#f0f0f0", text="Download Videos", command=self.download_videos)
        self.download_button.place(x=480, y=10, width=110, height=30)

        self.progress_text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
        self.progress_text.place(x=10, y=50, width=580, height=240)

    def extract_playlist_info(self, playlist_url):
        try:
            playlist = Playlist(playlist_url)
            videos_info = []
            self.update_progress(f"Extracting information from playlist: {playlist.title}")
            for i, video in enumerate(playlist.videos):
                video_info = {
                    "id": video.video_id,
                    "title": video.title,
                    "formats": video.streams.filter(progressive=True, file_extension='mp4').all()
                }
                videos_info.append(video_info)
                self.update_progress(f"Processed video {i+1}/{len(playlist.videos)}: {video.title}")
            return videos_info
        except Exception as e:
            self.update_progress(f"An error occurred: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def save_to_file(self, video_info, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for i, video_info in enumerate(video_info):
                    video_title = video_info["title"].replace(" ", "%20")
                    video_id = video_info["id"]
                    
                    # Try to get the requested quality, if not available, get the highest available quality
                    selected_format = None
                    available_qualities = [fmt.resolution for fmt in video_info['formats']]
                    
                    if self.quality_var.get() in available_qualities:
                        selected_format = next(fmt for fmt in video_info['formats'] if fmt.resolution == self.quality_var.get())
                    else:
                        selected_format = max(video_info['formats'], key=lambda x: int(x.resolution[:-1]) if x.resolution else 0)
                    
                    if selected_format:
                        video_url = selected_format.url
                        concatenated_info = f"{video_url}&title={video_title}"
                        f.write(concatenated_info + '\n')
                        self.update_progress(f"Saved info for video {i+1}/{len(video_info)}: {video_info['title']} ({selected_format.resolution})")
                    else:
                        self.update_progress(f"No suitable format found for: {video_info['title']}")
        except Exception as e:
            self.update_progress(f"An error occurred while saving to file: {str(e)}")
            messagebox.showerror("Error", f"An error occurred while saving to file: {str(e)}")

    def download_videos(self):
        playlist_url = self.playlist_entry.get()
        if not playlist_url:
            messagebox.showwarning("Warning", "Please enter a playlist URL")
            return
        filename = "playlist.txt"
        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.delete(1.0, tk.END)
        self.progress_text.config(state=tk.DISABLED)
        self.update_progress("Starting download process...")
        videos_info = self.extract_playlist_info(playlist_url)
        if videos_info:
            self.save_to_file(videos_info, filename)
            self.update_progress(f"Playlist information saved to {filename}")
            messagebox.showinfo("Success", f"Playlist information saved to {filename}")

    def update_progress(self, message):
        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.insert(tk.END, message + "\n")
        self.progress_text.see(tk.END)
        self.progress_text.config(state=tk.DISABLED)
        self.progress_text.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()