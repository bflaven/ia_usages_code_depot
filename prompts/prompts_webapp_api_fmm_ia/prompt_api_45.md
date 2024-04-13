# prompt_api_46.md

## prompt_1
As an advanced programmer, enhance with CSS the code below, you can leverage on existing boilerplate style forma cdn



# output
Here's a basic HTML, CSS, and JavaScript code that implements the described functionality:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audio Player with Transcript</title>
    <style>
        #container {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin: 20px;
        }
        #transcript {
            width: 45%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <div id="container">
        <audio id="audioPlayer" controls>
            <source src="CHR_MAMANE_08_02.mp3" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        <div id="transcript"></div>
    </div>

    <script>
        const transcriptData = [
            { "time": "0:00", "text": "Hello," },
            { "time": "0:02", "text": "how" },
            { "time": "0:03", "text": "are" },
            { "time": "0:04", "text": "you?" }
            // Add more transcript data as needed
        ];

        const audioPlayer = document.getElementById('audioPlayer');
        const transcriptDiv = document.getElementById('transcript');

        // Load transcript
        transcriptData.forEach(line => {
            const span = document.createElement('span');
            span.textContent = line.text + ' ';
            transcriptDiv.appendChild(span);
        });

        // Highlight words as the audio plays
        audioPlayer.addEventListener('timeupdate', function() {
            const currentTime = audioPlayer.currentTime;
            transcriptData.forEach(line => {
                const [min, sec] = line.time.split(':').map(parseFloat);
                const timeInSeconds = min * 60 + sec;
                const span = transcriptDiv.querySelector(`span[data-time="${line.time}"]`);
                if (span) {
                    if (currentTime >= timeInSeconds && currentTime < timeInSeconds + 2) {
                        span.style.backgroundColor = 'yellow'; // Highlight current word
                    } else {
                        span.style.backgroundColor = 'transparent'; // Remove highlight
                    }
                }
            });
        });

        // Reset transcript highlights when audio ends
        audioPlayer.addEventListener('ended', function() {
            transcriptDiv.querySelectorAll('span').forEach(span => {
                span.style.backgroundColor = 'transparent';
            });
        });
    </script>
</body>
</html>
```

This code sets up an HTML page with an audio player on the left and a transcript on the right. It loads the transcript data from a JSON-like array. As the audio plays, it highlights the corresponding word in the transcript. You can add more transcript data to the `transcriptData` array as needed. Make sure to replace `"audio_test.mp3"` with your audio file name, and update the transcript data accordingly.


Certainly! If you have a JSON file with your transcript data, you can load it using JavaScript. Here's how you can modify the script to load the transcript data from a JSON file:

Let's assume you have a file named `transcript.json` with the following content:

```json
[
    { "time": "0:00", "text": "Hello," },
    { "time": "0:02", "text": "how" },
    { "time": "0:03", "text": "are" },
    { "time": "0:04", "text": "you?" }
]
```

You can then modify the script to fetch this JSON file and use its content as the transcript data:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audio Player with Transcript</title>
    <style>
        #container {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin: 20px;
        }
        #transcript {
            width: 45%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <div id="container">
        <audio id="audioPlayer" controls>
            <source src="audio_test.mp3" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        <div id="transcript"></div>
    </div>

    <script>
        fetch('transcript.json')
            .then(response => response.json())
            .then(transcriptData => {
                const audioPlayer = document.getElementById('audioPlayer');
                const transcriptDiv = document.getElementById('transcript');

                // Load transcript
                transcriptData.forEach(line => {
                    const span = document.createElement('span');
                    span.textContent = line.text + ' ';
                    span.dataset.time = line.time; // Set custom attribute to store time
                    transcriptDiv.appendChild(span);
                });

                // Highlight words as the audio plays
                audioPlayer.addEventListener('timeupdate', function() {
                    const currentTime = audioPlayer.currentTime;
                    transcriptData.forEach(line => {
                        const [min, sec] = line.time.split(':').map(parseFloat);
                        const timeInSeconds = min * 60 + sec;
                        const span = transcriptDiv.querySelector(`span[data-time="${line.time}"]`);
                        if (span) {
                            if (currentTime >= timeInSeconds && currentTime < timeInSeconds + 2) {
                                span.style.backgroundColor = 'yellow'; // Highlight current word
                            } else {
                                span.style.backgroundColor = 'transparent'; // Remove highlight
                            }
                        }
                    });
                });

                // Reset transcript highlights when audio ends
                audioPlayer.addEventListener('ended', function() {
                    transcriptDiv.querySelectorAll('span').forEach(span => {
                        span.style.backgroundColor = 'transparent';
                    });
                });
            })
            .catch(error => console.error('Error fetching transcript data:', error));
    </script>
</body>
</html>
```

Make sure that `transcript.json` is in the same directory as your HTML file. This script fetches the JSON file using the Fetch API, parses it, and then uses the transcript data to populate the transcript on the webpage.


# prompt

Take ths json structure below and change the script to make it work

{
  "language": "fr",
  "language_probability": 0.9656448364257812,
  "segments": [
    {
      "start": 0,
      "end": 1.28,
      "words": [
        {
          "start": 0,
          "end": 0.38,
          "word": " Joseph"
        },
        {
          "start": 0.38,
          "end": 0.7,
          "word": " Antoine"
        },
        {
          "start": 0.7,
          "end": 0.84,
          "word": " Bell"
        },
        {
          "start": 0.84,
          "end": 1.28,
          "word": " bonjour."
        }
      ]
    },
    {
      "start": 1.52,
      "end": 2.78,
      "words": [
        {
          "start": 1.52,
          "end": 1.88,
          "word": " Bonjour"
        },
        {
          "start": 1.88,
          "end": 2.38,
          "word": " Christophe"
        },
        {
          "start": 2.38,
          "end": 2.78,
          "word": " Jusset."
        }
      ]
    }
  ]
}


To integrate the provided JSON structure into the transcript display and audio synchronization, we need to adjust the script to parse the JSON data accordingly. Here's the updated script:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audio Player with Transcript</title>
    <style>
        #container {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin: 20px;
        }
        #transcript {
            width: 45%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <div id="container">
        <audio id="audioPlayer" controls>
            <source src="audio_test.mp3" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        <div id="transcript"></div>
    </div>

    <script>
        fetch('transcript.json')
            .then(response => response.json())
            .then(data => {
                const audioPlayer = document.getElementById('audioPlayer');
                const transcriptDiv = document.getElementById('transcript');

                const segments = data.segments;

                // Load transcript
                segments.forEach(segment => {
                    segment.words.forEach(word => {
                        const span = document.createElement('span');
                        span.textContent = word.word + ' ';
                        span.dataset.start = word.start; // Set custom attribute to store start time
                        span.dataset.end = word.end; // Set custom attribute to store end time
                        transcriptDiv.appendChild(span);
                    });
                });

                // Highlight words as the audio plays
                audioPlayer.addEventListener('timeupdate', function() {
                    const currentTime = audioPlayer.currentTime;
                    transcriptDiv.querySelectorAll('span').forEach(span => {
                        const startTime = parseFloat(span.dataset.start);
                        const endTime = parseFloat(span.dataset.end);
                        if (currentTime >= startTime && currentTime <= endTime) {
                            span.style.backgroundColor = 'yellow'; // Highlight current word
                        } else {
                            span.style.backgroundColor = 'transparent'; // Remove highlight
                        }
                    });
                });

                // Reset transcript highlights when audio ends
                audioPlayer.addEventListener('ended', function() {
                    transcriptDiv.querySelectorAll('span').forEach(span => {
                        span.style.backgroundColor = 'transparent';
                    });
                });
            })
            .catch(error => console.error('Error fetching transcript data:', error));
    </script>
</body>
</html>
```

This script fetches the JSON file containing the transcript data, parses it, and then populates the transcript on the webpage. It iterates over each segment and its corresponding words, creating spans for each word with their start and end times. Then, it synchronizes the transcript with the audio player by highlighting the words being spoken as the audio plays.