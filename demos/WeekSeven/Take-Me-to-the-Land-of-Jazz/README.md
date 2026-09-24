# Take Me to the Land of Jazz

An interactive p5.js brushstroke animation and a synchronized 2:44 video made for the supplied recording. The visuals are a playful reading of the 1919 song rather than a historical reconstruction.

## Play

Open `index.html` in a browser. If the browser blocks audio from local files, start a local server in this folder, then visit its address:

```sh
python3 -m http.server 8000
```

Press **Play**, drag the timeline to visit any scene, press **Space** to pause or resume, or hide the scene notes. The packaged p5 library and audio keep the piece self-contained.

## Storyboard

| Time | Painted scene | Lyric or musical cue |
| --- | --- | --- |
| 0:00–0:03 | Spinning record | Quiet lead-in |
| 0:03–0:14 | Singing suitcase, Tennessee river | Verse begins |
| 0:14–0:27 | Escaping piano notes | Jazzy melody |
| 0:27–0:50 | Cabaret parade | Cabaret and the lead-up to the chorus |
| 0:50–1:03 | Memphis riverboat | Land of Jazz / Memphis blues |
| 1:03–1:13 | Tap dancing shoes | Ginger and pep |
| 1:13–1:24 | Swirling dancer | Razz-ma-tazz |
| 1:24–1:37 | Wind full of notes | Music in each breeze |
| 1:37–1:53 | Trombones growing on a tree | Second verse |
| 1:53–2:06 | Dancing duet | Join the fun |
| 2:06–2:19 | Train with a tune in tow | Chorus returns |
| 2:19–2:32 | Clock and moon | The warning about morning |
| 2:32–2:42 | Band and confetti | Final flourish |
| 2:42–2:44 | Painted end card | Record fades |

Scene motions read the supplied recording’s loudness map, `audio/analysis.json`. Playback time is always taken from the audio element, so seeking and pausing keep the picture synchronized. The brush drawing code is in `sketch.js`.

The recurring cast sings, blinks, looks around, dances, and reacts to changes in the recording’s intensity. The suitcase, dancers, shoes, riverboat, train, and clock each get their own little performance.

Music: “Take Me to the Land of Jazz” (1919), music by Pete Wendling and words by Bert Kalmar and Edgar Leslie. [Archived sheet music and lyrics](https://egrove.olemiss.edu/sharris_c/163/). Recording: supplied by Anastasia Salter.
