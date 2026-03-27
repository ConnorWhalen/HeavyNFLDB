
function createArtistLI(artist, feed) {
    const li = document.createElement('li');
    li.classList.add('song-li');
    li.innerHTML = (
        '<span class="song-li-left">' +
            '<div class="song-li-thumb-cover">' +
                `<img class="song-li-thumb" src="https://assets.heavynfldb.ca/thumbnails/${artist.thumb_video_id}/hqdefault.jpg"/>` +
            '</div>' +
        '</span>' +
        '<span class="song-li-centre">' +
            `<div class="song-li-title">${artist.name}</div>` +
            `<div class="song-li-subtitle">${artist.hometowns}</div>` +
            `<div class="song-li-subtitle">${artist.genres}</div>` +
        '</span>'
    );
    feed.appendChild(li);

    $(li).on('click', artist, (event) => {createArtistPreview(event.data);});
}

function createArtistPreview(artist) {
    const preview = document.getElementById('artist-preview')
    preview.replaceChildren();
    preview.innerHTML = (
        '<div id="artist-preview-close">' +
            closeIcon(24) +
        '</div>' +
        `<div class="song-preview-thumb-cover">` +
            `<img class="song-preview-thumb" src="https://assets.heavynfldb.ca/thumbnails/${artist.thumb_video_id}/hqdefault.jpg"></img>` +
        '</div>'
    );
    preview.innerHTML += (
        '<div class="song-preview-title">' +
            `${artist.name}` +
        '</div>' +
        '<br/>'
    );
    preview.innerHTML += `${artist.hometowns}<br/>${artist.genres}<br/><br/>`;
    for (let i = 0; i < artist.albums.length; i++) {
        preview.innerHTML += (
            `<div class="song-preview-subtitle">` +
                `<span class="song-preview-icon-left artist-preview-album" album-id="${artist.album_ids[i]}">${arrowIcon(36)}</span>` +
                `${artist.albums[i]}` +
            '</div>'
        );
    }
    preview.style.display = 'block';

    $('#artist-preview-close').on('click', (event) => {preview.style.display = 'none';});
    $('.artist-preview-album').on('click', function(event) {createAlbumPreviewById(parseInt($(this).attr('album-id')));});
}

function createArtistPreviewById(artist_id) {
    const artist = artists.find((a) => a.id === artist_id);
    createArtistPreview(artist);
}
