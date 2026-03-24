
function videoPlayer(video, video_player) {
    if(Hls.isSupported()) {
        const hls = new Hls();
        hls.loadSource(`assets.heavynfldb.ca/video_streams/${video.id}/playlist.m3u8`);
        hls.attachMedia(video_player);
        hls.on(Hls.Events.MANIFEST_PARSED, function() {
            video_player.play();
        });
    }
    else if (video_player.canPlayType('application/vnd.apple.mpegurl')) {
        video_player.src = `assets.heavynfldb.ca/video_streams/${video.id}/playlist.m3u8`;
        video_player.addEventListener('canplay', function() {
            video_player.play();
        });
    }
    else {
        console.log("HLS video not supported!");
    }
}


function playVideo(video) {
    const player = document.getElementById('video-player');

    if (player.getAttribute('video-id') === video.id.toString()) return;
    else console.log('NOT SKIPPING');

    player.innerHTML = (
        '<div id="video-player-close">' +
            closeIcon(24) +
        '</div>' +
        '<video id=vid-player controls></video>' +
        `<div id=video-player-title class="video-player-title">${video.title}</div>` +
        `<div id=video-player-date class="video-player-subtitle">${readableDate(video.upload_date)}</div>` +
        `<div id=video-player-album class="video-player-subtitle">${video.description}</div>`
    );
    player.style.display = 'block';
    player.setAttribute('video-id', video.id);

    const video_player = document.getElementById('vid-player');
    videoPlayer(video, video_player);

    $('#video-player-close').on('click', (event) => {
        video_player.pause();
        player.style.display = 'none';
        player.removeAttribute('video-id');
    });
}

function createVideoLI(video, feed) {
    const li = document.createElement('li');
    li.classList.add('song-li');
    li.innerHTML = (
        '<span class="song-li-left">' +
            '<div class="song-li-thumb-cover">' +
                `<img class="song-li-thumb" src="assets.heavynfldb.ca/thumbnails/${video.id}/hqdefault.jpg"/>` +
            '</div>' +
        '</span>' +
        '<span class="song-li-centre">' +
            `<div class="song-li-title">${video.title}</div>` +
            `<div class="song-li-subtitle">${readableDate(video.upload_date)}</div>` +
        '</span>' +
        `<span class="song-li-right" video-id="${video.id}">` +
            playIcon(64) +
        '</span>'
    );
    feed.appendChild(li);

    $(li).on('click', video, (event) => {createVideoPreview(event.data);});
    $(`.song-li-right[video-id="${video.id}"]`).on('click', video, (event) => {event.stopPropagation(); playVideo(event.data);});
}

function createVideoPreview(video) {
    const preview = document.getElementById('video-preview')
    preview.replaceChildren();
    preview.innerHTML = (
        '<div id="video-preview-close">' +
            closeIcon(24) +
        '</div>' +
        `<div class="song-preview-thumb-cover">` +
            `<img class="song-preview-thumb" src="assets.heavynfldb.ca/thumbnails/${video.id}/hqdefault.jpg"></img>` +
        '</div>'
    );
    preview.innerHTML += `${video.title}<br/>${video.upload_date}<br/><br/>${video.description}`;
    preview.style.display = 'block';

    $('#video-preview-close').on('click', (event) => {preview.style.display = 'none';});
}