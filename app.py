from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import subprocess

app = Flask(__name__)

# Define directories where audiobooks and music CDs will be saved
AUDIOBOOKS_DIR = './audiobooks'  # Set your desired save directory for audiobooks
MUSIC_DIR = './music'  # Set your desired save directory for music CDs


# Helper function to get list of artist folders for autocomplete
def get_artist_names():
    if os.path.exists(MUSIC_DIR):
        return [
            d for d in os.listdir(MUSIC_DIR)
            if os.path.isdir(os.path.join(MUSIC_DIR, d))
        ]
    return []


# Home page with options for Audiobook or Music CD ripping
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Audiobook ripping workflow
@app.route('/audiobook', methods=['GET', 'POST'])
def audiobook():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        audiobook_path = os.path.join(AUDIOBOOKS_DIR, author, title)
        os.makedirs(audiobook_path, exist_ok=True)
        return redirect(
            url_for('rip_disc',
                    media_type='audiobook',
                    author=author,
                    title=title,
                    disc_number=1))
    return render_template('audiobook.html')


# Music CD ripping workflow
@app.route('/music', methods=['GET', 'POST'])
def music():
    if request.method == 'POST':
        album = request.form['album']
        artist = request.form['artist']
        music_path = os.path.join(MUSIC_DIR, artist, album)
        os.makedirs(music_path, exist_ok=True)
        return redirect(
            url_for('rip_disc',
                    media_type='music',
                    artist=artist,
                    album=album,
                    disc_number=1))
    return render_template('music.html', artists=get_artist_names())


# Endpoint to handle disc ripping
@app.route(
    '/rip_disc/<media_type>/<identifier_1>/<identifier_2>/<int:disc_number>',
    methods=['GET', 'POST'])
def rip_disc(media_type, identifier_1, identifier_2, disc_number):
    if request.method == 'POST':
        if media_type == 'audiobook':
            path = os.path.join(AUDIOBOOKS_DIR, identifier_1, identifier_2,
                                f"CD{disc_number}")
        else:  # media_type == 'music'
            path = os.path.join(MUSIC_DIR, identifier_1, identifier_2,
                                f"CD{disc_number}")

        os.makedirs(path, exist_ok=True)
        rip_command = f'cdparanoia -B "{path}/track.wav"'
        subprocess.run(rip_command, shell=True, check=True)
        return redirect(
            url_for('rip_disc',
                    media_type=media_type,
                    identifier_1=identifier_1,
                    identifier_2=identifier_2,
                    disc_number=disc_number + 1))

    return render_template('rip_disc.html',
                           media_type=media_type,
                           identifier_1=identifier_1,
                           identifier_2=identifier_2,
                           disc_number=disc_number)


# API endpoint for artist name autocomplete
@app.route('/api/artists', methods=['GET'])
def api_artists():
    return jsonify(get_artist_names())


# Finish the ripping process
@app.route('/finish')
def finish():
    return "Ripping process completed. You may now close the application."


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
