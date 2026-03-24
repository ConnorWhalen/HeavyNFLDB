
function createSongLI(song, feed) {
    const li = document.createElement('li');
    li.classList.add('song-li');
    li.innerHTML = (
        '<span class="song-li-left">' +
            '<div class="song-li-thumb-cover">' +
                `<img class="song-li-thumb" src="assets.heavynfldb.ca/thumbnails/${song.video_id}/hqdefault.jpg"/>` +
            '</div>' +
        '</span>' +
        '<span class="song-li-centre">' +
            `<div class="song-li-title">${song.title}</div>` +
            `<div class="song-li-subtitle">${song.artist} - ${song.album}</div>` +
        '</span>' +
        `<span class="song-li-right" song-id="${song.id}">` +
            playIcon(64) +
        '</span>'
    );
    feed.appendChild(li);

    $(li).on('click', song, (event) => {createSongPreview(event.data);});
    $(`.song-li-right[song-id="${song.id}"]`).on('click', song, (event) => {event.stopPropagation(); playSong(event.data);});
}

function createSongPreview(song) {
    const preview = document.getElementById('song-preview')
    preview.replaceChildren();
    preview.innerHTML = (
        '<div id="song-preview-close">' +
            closeIcon(24) +
        '</div>' +
        `<div class="song-preview-thumb-cover">` +
            `<img class="song-preview-thumb" src="assets.heavynfldb.ca/thumbnails/${song.video_id}/hqdefault.jpg"></img>` +
        '</div>'
    );
    preview.innerHTML += `${song.title}<br/>${song.artist}<br/>${song.album}<br/>${song.release_date}<br/>${song.genre}<br/>${song.hometown}<br/>${song.label}`
    preview.style.display = 'block';

    $('#song-preview-close').on('click', (event) => {preview.style.display = 'none';});
}

function playSong(song) {
    const player = document.getElementById('song-player');

    if (player.getAttribute('song-id') === song.id.toString()) return;
    else console.log('NOT SKIPPING');

    player.innerHTML = (
        '<div id="song-player-close">' +
            closeIcon(24) +
        '</div>' +
        '<span class="song-li-left">' +
            '<div class="song-player-thumb-cover">' +
                `<img class="song-li-thumb" src="assets.heavynfldb.ca/thumbnails/${song.video_id}/hqdefault.jpg"/>` +
            '</div>' +
        '</span>' +
        '<span class="song-li-centre">' +
            `<div id=song-player-title class="song-li-title">${song.title}</div>` +
            `<div id=song-player-artist class="song-li-title">${song.artist}</div>` +
            `<div id=song-player-album class="song-li-subtitle">${song.album}</div>` +
        '</span>' +
        '<audio id=audio-player controls controlsList="noplaybackrate"></audio>'
    );
    player.style.display = 'block';
    player.setAttribute('song-id', song.id);

    const audio = document.getElementById('audio-player');
    audio.setAttribute('src', `assets.heavynfldb.ca/streams/${song.video_id}/playlist.m3u8`);
    audio.play()

    $('#song-player-close').on('click', (event) => {
        audio.pause();
        player.style.display = 'none';
        player.removeAttribute('song-id');
    });
}