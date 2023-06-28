import os
from flask import Flask, render_template, request, jsonify, send_file
from music21 import converter, note

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the uploaded file from the request
        file = request.files['file']

        # Save the uploaded file temporarily
        temp_filepath = 'temp.musicxml'
        file.save(temp_filepath)

        # Parse the MusicXML file
        parsed_work = converter.parse(temp_filepath)
        recurse_work = parsed_work.recurse()

        # Iterate through the notes and add the extraction data as lyrics
        for i, note_obj in enumerate(recurse_work.notes):
            extraction_data = (note_obj.step, note_obj.octave)
            new_lyric = note.Lyric(str(extraction_data))  # Convert the extraction data to a string
            note_obj.lyrics.append(new_lyric)

        # Generate the output
        output_filename = 'revised.xml'
        parsed_work.write('musicxml', fp=output_filename)

        # Remove the temporary file
        os.remove(temp_filepath)

        # Return the file as a downloadable attachment
        return send_file(output_filename, as_attachment=True)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)