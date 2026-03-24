
function songsSearch(value) {
    let result = null;
    if (value && value.length > 1) {
        result = song_index.search(searchQuery(value));
    }

    const result_songs = applySearch(
        result,
        songs,
        (a, b) => compNullsLast(a.sort_date, b.sort_date, (c, d) => d.localeCompare(c))
    );
    
    setMainFeed(result_songs, (song, feed) => createSongLI(song, feed));
}

function albumsSearch(value) {
    let result = null;
    if (value && value.length > 1) {
        result = album_index.search(searchQuery(value));
    }

    const result_albums = applySearch(
        result,
        albums,
        (a, b) => a.name.localeCompare(b.name)
    );
    
    setMainFeed(result_albums, (album, feed) => createAlbumLI(album, feed));
}

function artistsSearch(value) {
    let result = null;
    if (value && value.length > 1) {
        result = artist_index.search(searchQuery(value));
    }

    const result_artists = applySearch(
        result,
        artists,
        (a, b) => a.name.localeCompare(b.name)
    );
    
    setMainFeed(result_artists, (artist, feed) => createArtistLI(artist, feed));
}

function videosSearch(value) {
    let result = null;
    if (value && value.length > 1) {
        result = video_index.search(searchQuery(value));
    }

    const result_videos = applySearch(
        result,
        videos,
        (a, b) => b.upload_date.localeCompare(a.upload_date)
    );
    
    setMainFeed(result_videos, (video, feed) => createVideoLI(video, feed));
}

function applySearch(result, objs, default_sort_func) {
    let result_objs = objs;
    if (result && result.length > 0) {
        result_objs = result_objs.filter((obj) => result.findIndex((res) => res.ref === obj.id.toString()) > -1);
        result_objs.sort(
            (a, b) => compNegativesLast(
                result.findIndex((res) => res.ref === a.id.toString()),
                result.findIndex((res) => res.ref === b.id.toString()),
                (c, d) => d < c
            )
        );
    }
    else if (result === null) {
        result_objs.sort(default_sort_func);
    }
    else {
        result_objs = []
    }

    return result_objs;
}

function searchQuery(value) {
    if (value.length > 3) {
        return `${value}~1`;
    }
    return `${value}`;
}
