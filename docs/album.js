
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
    preview.innerHTML += `${album.name}<br/>${album.artists}<br/><br/>`;
    for (let i = 0; i < album.songs.length; i++) {
        preview.innerHTML += `${album.songs[i]}</br/>`;
    }
    preview.style.display = 'block';

    $('#album-preview-close').on('click', (event) => {preview.style.display = 'none';});
}
