# Zenfix VLC — Pro Compact + Glass

This repository builds a custom Windows x64 VLC based on the upstream VideoLAN VLC source code.

## Design target

- Native VLC Qt/QML interface, not a skins2 `.vlt` skin and not a PowerShell wrapper.
- Left vertical menu: Media, Playback, Audio, Video, Subtitles, Tools, View, Help.
- Central video area.
- Docked translucent playlist on the right.
- Bottom quick controls: Audio Track, Subtitles, Playback Speed, Chapters.
- Native VLC playback controls, volume, seek bar and fullscreen.
- Windowed UI uses VLC's native acrylic/frosted-glass primitives.
- Fullscreen hides Zenfix side panels to maximize video.

The build is pinned to a specific upstream VLC commit for reproducibility.
