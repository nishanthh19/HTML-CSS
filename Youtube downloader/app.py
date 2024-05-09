from flask import Flask, render_template, request, send_file, session
from flask_session import Session
from pytube import YouTube
from io import BytesIO

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
	return render_template("index.html", data=None)
	
@app.route("/index", methods=["POST", "GET"])
def fetchVideo():
	if request.method == "POST":
		url = request.form["videourl"]
		if url:
			yt = YouTube(url)
			title = yt.title
			thumbnail = yt.thumbnail_url
			streams = yt.streams.filter(file_extension='mp4')
			data = [title, thumbnail, streams, url]
			session["video"] = yt
			
			return render_template("index.html", data=data)

@app.route("/download/", methods=["POST", "GET"])
def downloadVideo():
		itag = request.args.get("itag", None)
		name = session["video"].title
		video = session["video"].streams.get_by_itag(str(itag))
		buffer = BytesIO()
		video.stream_to_buffer(buffer)
		buffer.seek(0)

		return send_file(
			buffer,
			as_attachment=True,
			attachment_filename=name,
			mimetype="video/mp4",
		)
	
# https://youtu.be/jiY4PgUW7aA
if __name__ == "__main__":
	app.run(debug=True)