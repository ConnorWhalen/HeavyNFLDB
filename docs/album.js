
function createAlbumLI(album, feed) {
    const li = document.createElement('li');
    li.classList.add('song-li');
    li.innerHTML = (
        '<span class="song-li-left">' +
            '<div class="song-li-thumb-cover">' +
                `<img class="song-li-thumb" src="https://assets.heavynfldb.ca/thumbnails/${album.thumb_video_id}/hqdefault.jpg"/>` +
            '</div>' +
        '</span>' +
        '<span class="song-li-centre">' +
            `<div class="song-li-title">${album.name}</div>` +
            `<div class="song-li-subtitle">${album.artists}</div>` +
        '</span>'
    );
    feed.appendChild(li);

    $(li).on('click', album, (event) => {createAlbumPreview(event.data);});
}

function createAlbumPreview(album) {
    const preview = document.getElementById('album-preview')
    preview.replaceChildren();
    preview.innerHTML = (
        '<div id="album-preview-close">' +
            closeIcon(24) +
        '</div>' +
        `<div class="song-preview-thumb-cover">` +
            `<img class="song-preview-thumb" src="https://assets.heavynfldb.ca/thumbnails/${album.thumb_video_id}/hqdefault.jpg"></img>` +
        '</div>'
    );
    preview.innerHTML += (
        '<div class="song-preview-title">' +
            `${album.name}` +
        '</div>' +
        '<br/>'
    );
    for (let i = 0; i < album.artists.length; i++) {
        preview.innerHTML += (
            `<div class="song-preview-subtitle">` +
                `<span class="song-preview-icon-left">${profileIcon(24)}</span>` +
                `${album.artists[i]}` +
                `<span class="song-preview-icon-right album-preview-artist" artist-id="${album.artist_ids[i]}">${arrowIcon(48)}</span>` +
            '</div>'
        );
    }
    preview.innerHTML += '<br/>';
    for (let i = 0; i < album.songs.length; i++) {
        preview.innerHTML += (
            `<div class="song-preview-subtitle">` +
                `<span class="song-preview-icon-left album-preview-song" song-id="${album.song_ids[i]}">${arrowIcon(36)}</span>` +
                `${album.songs[i]}` +
            '</div>'
        );
    }
    preview.style.display = 'block';

    $('#album-preview-close').on('click', (event) => {preview.style.display = 'none';});
    $('.album-preview-artist').on('click', function(event) {createArtistPreviewById(parseInt($(this).attr('artist-id')));});
    $('.album-preview-song').on('click', function(event) {createSongPreviewById(parseInt($(this).attr('song-id')));});
}

function createAlbumPreviewById(album_id) {
    const album = albums.find((a) => a.id === album_id);
    createAlbumPreview(album);
}
