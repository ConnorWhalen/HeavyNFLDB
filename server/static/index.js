function ytClick(url) {
    let yt_embed = document.getElementById("yt-embed");

    yt_embed.removeAttribute("srcdoc");
    yt_embed.setAttribute("src", url);
}

function loadPage() {
    let subpage = document.getElementById("subpage")
    
    subpage.innerHTML = "";
    
    const paramsString = window.location.search;
    const searchParams = new URLSearchParams(paramsString);

    if (searchParams.has("artist")) {
        loadArtist(subpage, searchParams.get("artist"));
    }
    else if (searchParams.has("album")) {
        loadAlbum(subpage, searchParams.get("album"));
    }
    else {
        loadTable(subpage);
    }
}

function artistClick(artistId) {
    window.history.pushState({}, document.title, `/?artist=${artistId}`);
    loadPage()
}

function albumClick(albumId) {
    window.history.pushState({}, document.title, `/?album=${albumId}`);
    loadPage()
}

function tableClick() {
    window.history.pushState({}, document.title, '/');
    loadPage()
}

function loadArtist(subpage, artistId) {
    $(subpage).load(`/artist/${artistId}`)
}

function loadAlbum(subpage, albumId) {
    $(subpage).load(`/album/${albumId}`)
}

function loadTable(subpage) {
    $(subpage).load("/table", function() {
        $('#myTable').DataTable({
            serverSide: true,
            scrollX: true,
            ajax: {
                url: '/api/songs',
                dataSrc: 'data',
            },
            columns: [
                { data: 'title' },
                { data: 'artist' },
                { data: 'album' },
                { data: 'hometown' },
                { data: 'release_date' },
                { data: 'genre' },
                { data: 'label' },
                { data: 'video_url'}
            ],
            columnDefs: [
                {
                    "targets": 1,
                    "data": "artist",
                    "render": function ( data, type, row, meta ) {
                        return '<div onclick="artistClick(\''+row['artist_id']+'\')" class="artist-link"><u>'+data+'</u></div>';
                    }
                },
                {
                    "targets": 2,
                    "data": "album",
                    "render": function ( data, type, row, meta ) {
                        return '<div onclick="albumClick(\''+row['album_id']+'\')" class="album-link"><u>'+data+'</u></div>';
                    }
                },
                {
                    "targets": 7,
                    "data": "video_url",
                    "render": function ( data, type, row, meta ) {
                        // return '<a href="'+data+'" target="_blank">'+data+'</a>';
                        return '<div onclick="ytClick(\'' + data + '\')" class="yt-link"><u>[YouTube]</u></div>';
                    }
                }
            ],
            order: [[4, 'desc']],
            initComplete: function () {
                this.api()
                    .columns()
                    .every(function () {
                        let column = this;
                        let title = column.footer().textContent;
         
                        // Create input element
                        let input = document.createElement('input');
                        input.classList.add('column-input');
                        input.placeholder = title;
                        column.footer().replaceChildren(input);
         
                        // Event listener for user input
                        input.addEventListener('keyup', () => {
                            if (column.search() !== this.value) {
                                column.search(input.value).draw();
                            }
                        });
                    });
            }
        });
    } );
}

$(document).ready(function () {
    loadPage();
});
