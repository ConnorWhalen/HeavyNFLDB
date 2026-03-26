
const PAGE_SIZE = 100;

async function loadIndex(name) {
    const resp = await fetch(`https://assets.heavynfldb.ca/data/${name}_idx.json.gz`);
    const serializedIndex = await resp.json();
    return lunr.Index.load(serializedIndex);
}

async function loadList(name) {
    const resp = await fetch(`https://assets.heavynfldb.ca/data/${name}.json.gz`);
    return await resp.json();
}

let song_index = undefined;
let album_index = undefined;
let artist_index = undefined;
let video_index = undefined;

let songs = undefined;
let albums = undefined;
let artists = undefined;
let videos = undefined;

let mainFeed = undefined;
let mainFeedList = undefined;
let mainFeedLIFunc = undefined;
let mainFeedSearchFunc = undefined;
let mainFeedPage = undefined;

$(document).ready(async function () {
    song_index = await loadIndex('song');
    album_index = await loadIndex('album');
    artist_index = await loadIndex('artist');
    video_index = await loadIndex('video');

    songs = await loadList('song');
    albums = await loadList('album');
    artists = await loadList('artist');
    videos = await loadList('video');
    album_artists = await loadList('album_artist');
    links = await loadList('link');

    mainFeed = document.getElementById('main-feed-list');

    $('#header-text').on('click', () => {songsClick(null);});
    songsClick(null);

    $('#main-search').on('input', function() {mainFeedSearchFunc($(this).val());});

    $('#main-search-close').on('click', () => {$('#main-search').val(''); mainFeedSearchFunc('');});
});

function setMainFeed(list, liFunc, searchFunc) {
    mainFeed.replaceChildren();
    mainFeedList = list;
    mainFeedLIFunc = liFunc;
    mainFeedPage = 0;
    setMainFeedPage();
    if (searchFunc) {
        mainFeedSearchFunc = searchFunc;
        searchFunc($('#main-search').val());
    }
}

function setMainFeedPage() {
    if (mainFeedPage * PAGE_SIZE > mainFeedList.length) {
        return;
    }
    console.log(`fetching ${mainFeedPage * PAGE_SIZE} to ${(mainFeedPage+1) * PAGE_SIZE} of ${mainFeedList.length}`);
    for (i = mainFeedPage * PAGE_SIZE; i < (mainFeedPage+1) * PAGE_SIZE; i++) {
        if (i >= mainFeedList.length) break;
        mainFeedLIFunc(mainFeedList[i], mainFeed);
    }
    mainFeedPage++;
}

$(window).on("scroll.once", function() {
    if ($(window).scrollTop() >= $(document).height() - $(window).height() - 5){
        setMainFeedPage();
    }
});
