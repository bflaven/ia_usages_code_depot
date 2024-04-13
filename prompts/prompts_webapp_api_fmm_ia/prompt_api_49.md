# prompt_api_49.md

## prompt_1
Fix the code below so the transcription play with the video when the user click on the play button.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audio Player with Transcript</title>
    <!-- Importing CSS from CDN -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css">
    <style>
        /* Custom styles */
        body {
            font-family: Arial, sans-serif;
        }
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
        #transcript span {
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        #audioPlayer {
            width: 50%;
            margin-right: 20px;
        }
        #videoPlayer {
            width: 50%; /* Set width to 100% of the container */
            height: auto; /* Automatically adjust height to maintain aspect ratio */
        }
    </style>
</head>
<body>

<!-- command -->
<!-- 

cd /Users/brunoflaven/Documents/02_copy/fmm_USECASES/_webapp_api_fmm_ia/005_webapp_api_fmm_ia/

python -m http.server 4000 

-->

    <div id="container">
    <video id="videoPlayer" controls width="640" height="360">
        <source src="data/videos/01_video_FR_20240215_110050_110458_CS_5000.mp4" type="video/mp4">
        Your browser does not support the video element.
    </video>
    <div id="transcript"></div>
</div>


    <script>
        fetch('data/videos/01_video_FR_20240215_110050_110458_CS_5000_whisper_express.json')
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


# output
To fix the code and synchronize the transcription with the video instead of an audio player, you need to make several adjustments:

1. Replace the `<audio>` element with the `<video>` element.
2. Adjust the event listeners to listen to the video's time updates and end events.
3. Ensure that when the user clicks the play button, the video plays and the transcription highlights the corresponding words.

Here's the modified code:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Player with Transcript</title>
    <!-- Importing CSS from CDN -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css">
    <style>
        /* Custom styles */
        body {
            font-family: Arial, sans-serif;
        }
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
        #transcript span {
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        #videoPlayer {
            width: 50%; /* Set width to 100% of the container */
            height: auto; /* Automatically adjust height to maintain aspect ratio */
        }
    </style>
</head>
<body>

<div id="container">
    <video id="videoPlayer" controls width="640" height="360">
        <source src="data/videos/01_video_FR_20240215_110050_110458_CS_5000.mp4" type="video/mp4">
        Your browser does not support the video element.
    </video>
    <div id="transcript"></div>
</div>

<script>
    fetch('data/videos/01_video_FR_20240215_110050_110458_CS_5000_whisper_express.json')
        .then(response => response.json())
        .then(data => {
            const videoPlayer = document.getElementById('videoPlayer');
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

            // Highlight words as the video plays
            videoPlayer.addEventListener('timeupdate', function() {
                const currentTime = videoPlayer.currentTime;
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

            // Reset transcript highlights when video ends
            videoPlayer.addEventListener('ended', function() {
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

With these modifications, the transcription will synchronize with the video, and the transcription highlights the words being spoken in the video as it plays.

