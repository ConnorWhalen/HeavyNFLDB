
function songsClick(event) {
    songs.sort((a, b) => compNullsLast(a.sort_date, b.sort_date, (c, d) => d.localeCompare(c)));

    const sample = songs; //.filter((song) => song.video_id === 'KMnWQ0fm-Zg' || song.video_id === 'kNFOrP8fqdA');
    
    setMainFeed(sample, (song, feed) => createSongLI(song, feed), songsSearch);
}

function albumsClick(event) {
    albums.sort((a, b) => a.name.localeCompare(b.name));
    
    setMainFeed(albums, (album, feed) => createAlbumLI(album, feed), albumsSearch);
}

function artistsClick(event) {
    artists.sort((a, b) => a.name.localeCompare(b.name));
    
    setMainFeed(artists, (artist, feed) => createArtistLI(artist, feed), artistsSearch);
}

function videosClick(event) {
    videos.sort((a, b) => b.upload_date.localeCompare(a.upload_date));
    
    setMainFeed(videos, (video, feed) => createVideoLI(video, feed), videosSearch);
}
